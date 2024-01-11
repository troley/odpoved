import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import home, file_upload
from app.db import models
from app.db.database import SessionLocal, engine
from app.util.file_creator import load_and_write_files_async
from app.util.paths import static_dir


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(home.router)
app.include_router(file_upload.router)

# When there are files already present in the DB, then write those files to dir. 
asyncio.create_task(load_and_write_files_async(SessionLocal()))
