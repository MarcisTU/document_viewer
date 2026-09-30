from datetime import date

from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql

from .enums import ImportanceLevel, FileType, DocumentCategory, ActiveStatus


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
    is_active: ActiveStatus


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
    is_active: ActiveStatus


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
    # need to tell sqlmodel to explicitly use the enum value since we have different language value for it
    is_active: ActiveStatus

    # is_active: ActiveStatus = Field(
    #     sa_column=Column(
    #         postgresql.ENUM(
    #             ActiveStatus,
    #             name="activestatus",
    #             values_callable=lambda enum: [member.value for member in enum],
    #         )
    #     )
    # )
