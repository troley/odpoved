from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.ai.llm import LLM
from app.config.templates import templates
from app.db import crud, schemas
from app.db.database import SessionLocal
from app.dependencies import get_db, get_llm
from app.util.file_creator import write_file_to_dir_async


router = APIRouter()


@router.get("/file_upload", response_class=HTMLResponse)
async def file_upload(request: Request):
    return templates.TemplateResponse(request=request, name="file_upload.html")

@router.post("/save_file", response_model=schemas.File)
async def save_file(file: schemas.FileCreate, db: SessionLocal = Depends(get_db), llm: LLM = Depends(get_llm)):
    fb_file = crud.get_file(db, file.name)
    if fb_file:
        raise HTTPException(status_code=400, detail="File already exists.")
   
    # Save new file into DB
    file = crud.create_file(db, schemas.FileCreate(name=file.name, content=file.content))
    
    # Save new file into directory for LLM to process
    await write_file_to_dir_async(file)
    
    # Re-initialize LLM with the new file
    llm.init_with_new_document(file.name)

    return file
