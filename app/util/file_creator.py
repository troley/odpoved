import base64
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import crud
from app.dependencies import get_db
from app.db.models import File
from .paths import files_dir


async def write_file_to_dir_async(file: File):
    """
    Writes a file to the pre-configured directory.

    Args:
        file (File): the file to write to the directory
    """
    with open(files_dir + file.name, "wb") as f:
        f.write(base64.b64decode(str(file.content).split(",", 1)[1]))

async def load_and_write_files_async(db: Session = Depends(get_db)):
    """
    Loads files from the data store and writes those to the pre-configured directory.
    If no files were loaded, then the write operation is a no-op.

    Args:
        db (Session, optional): the SQLAlchemy database session
    """
    files = crud.get_all_files(db)
    
    for file in files:
        await write_file_to_dir_async(file)
