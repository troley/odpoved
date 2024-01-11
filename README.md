# Odpoved

## Description
A hobby prototype [FAST API](https://fastapi.tiangolo.com/) web app utilizing [Python LangChain](https://python.langchain.com/) with [OpenAI](https://openai.com/) embeddings to answer questions based on information from PDF documents provided to it. Furthermore, the app utilizes [SQLite](https://www.sqlite.org/index.html) database (abstracted away by [SQLAlchemy](https://www.sqlalchemy.org/) ORM) for the storage of the PDF documents and the [Chroma](https://www.trychroma.com/) vector database for the storage of the document chunks.

The LLM has hard-coded instructions to answer in the Slovak language. The app front-end is also not i18n'd and only available in Slovak. Might change in the future (more things in the project require more effort).

## Install & run

- Have [Docker](https://www.docker.com/) installed (tested on version 24.x.x)

- `git clone` this project

- Be in the root directory, i.e.: `./odpoved`

- Build with `docker build -t project-odpoved/odpoved .`

<i>Do notice the `<your_openai_api_key>` below</I>.

- Run with `docker run -d --rm --name odpoved -e "OPENAI_API_KEY=<your_openai_api_key>" -p 80:8000 project-odpoved/odpoved`

- Access at `http://localhost`

### License
Odpoved is [MIT Licensed](./LICENSE)
