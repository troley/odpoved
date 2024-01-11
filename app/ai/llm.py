from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain.schema import format_document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_core.messages import get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.util.paths import files_dir


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")    

def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


class LLM():
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""
    
    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    
    Answer in the Slovak language."""
    
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
    ANSWER_PROMPT = ChatPromptTemplate.from_template(template)
    
    memory = ConversationBufferMemory(return_messages=True, output_key="answer", input_key="question")

    loaded_memory = RunnablePassthrough.assign(
        chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    
    standalone_question = {
    "standalone_question": {
        "question": lambda x: x["question"],
        "chat_history": lambda x: get_buffer_string(x["chat_history"]),
        }
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    }


    def __init__(self) -> None:
        """
        Primal initialization of the LLM and its vectore store. It loads documents from the
        `app/resources/files` directory and feeds it into the LLM's vectore store. The LLM will base
        its answers on the contents of the loaded documents.
        """
        
        self.retriever = self._get_retriever(self._get_documents())
        retrieved_documents = {
            "docs": itemgetter("standalone_question") | self.retriever,
            "question": lambda x: x["standalone_question"],
        }
        
        final_inputs = {
            "context": lambda x: _combine_documents(x["docs"]),
            "question": itemgetter("question"),
        }
        
        answer = {
            "answer": final_inputs | self.ANSWER_PROMPT | ChatOpenAI(),
            "docs": itemgetter("docs"),
        }
        
        self.chain = self.loaded_memory | self.standalone_question | retrieved_documents | answer

    def get_llm(self):
        return self.chain
    
    def get_memory(self):
        return self.memory
    
    def init_with_new_document(self, document_name):
        """
        Adds the new document to the LLM's vectore store and re-initializes the chain
        to make it up to date.

        Args:
            document_name (str): the name of the file in the `app/resources/files` directory, e.g.: my_file.pdf
        """
        self.retriever.add_documents(self._get_document(document_name))
        retrieved_documents = {
            "docs": itemgetter("standalone_question") | self.retriever,
            "question": lambda x: x["standalone_question"],
        }
        
        final_inputs = {
            "context": lambda x: _combine_documents(x["docs"]),
            "question": itemgetter("question"),
        }
        
        answer = {
            "answer": final_inputs | self.ANSWER_PROMPT | ChatOpenAI(),
            "docs": itemgetter("docs"),
        }
        
        self.chain = self.loaded_memory | self.standalone_question | retrieved_documents | answer
    
    def _get_documents(self):
        raw_documents = PyPDFDirectoryLoader(files_dir).load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        return text_splitter.split_documents(raw_documents)

    def _get_document(self, document_name):
        raw_documents = PyPDFLoader(files_dir + document_name).load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        return text_splitter.split_documents(raw_documents)
    
    def _get_retriever(self, documents):
        return Chroma.from_documents(documents, OpenAIEmbeddings()).as_retriever()


LLM = LLM()
