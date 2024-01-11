from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config.templates import templates
from app.db import crud
from app.dependencies import get_db
from app.dependencies import get_llm
from app.ai.llm import LLM
from .model.answer import Answer
from .model.question import Question


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    files = crud.get_all_files(db)
    return templates.TemplateResponse(request=request, name="home.html", context={"files": files})

@router.post("/question", response_model=Answer)
async def get_answer_to(question: Question, llm: LLM = Depends(get_llm)):
    answer = llm.get_llm().invoke({"question": question.question})["answer"].content
    
    # Save context into memory, so that the LLM remembers previous parts of the conversation.
    # Will be automated in the future. For now, has to happen manually according to LangChain docs.
    llm.get_memory().save_context({"question": question.question}, {"answer": answer})

    return Answer(answer=answer)
