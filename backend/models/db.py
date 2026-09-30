from datetime import date

from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel

from .enums import ImportanceLevel, FileType, DocumentCategory


### API puses modeļi kurus izmanto izveides vai apskates izsaukumos
class DocumentPublic(BaseModel):
    id: int
    name: str
    description: str
    responsible_unit: str
    creation_date: date
    url: HttpUrl
    file_type: FileType
    reading_time_minutes: int
    importance: ImportanceLevel
    category: DocumentCategory
    is_active: bool


class DocumentCreate(BaseModel):
    name: str
    description: str
    responsible_unit: str
    creation_date: date
    url: HttpUrl  
    file_type: FileType
    reading_time_minutes: int
    importance: ImportanceLevel
    category: DocumentCategory
    is_active: bool


### DB models
class Document(SQLModel, table=True):
    """"
    Satur XML saņemto lauku vērtības ar angļu valodas standartizētiem atribūtiem
    """

    __tablename__: str = "documents"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    responsible_unit: str
    creation_date: date
    url: str
    file_type: FileType
    reading_time_minutes: int
    importance: ImportanceLevel
    category: DocumentCategory
    is_active: bool
