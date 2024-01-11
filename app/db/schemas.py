from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    content: bytes

class File(FileBase):
    class Config:
        orm_mode = True

class FileCreate(FileBase):
    pass
