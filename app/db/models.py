from sqlalchemy import BLOB, Column, Integer, Text
from .database import Base


class File(Base):
    __tablename__ = "file"
    
    id = Column(Integer, primary_key=True,)
    name = Column(Text, index=True)
    content = Column(BLOB)
