from sqlalchemy.orm import Session

from . import models, schemas


def get_all_files(db: Session):
    return db.query(models.File).all()

def get_file(db: Session, file_name: str):
    return db.query(models.File).filter(models.File.name == file_name).first()

def create_file(db: Session, file: schemas.FileCreate):
    db_file = models.File(name=file.name, content=file.content)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
