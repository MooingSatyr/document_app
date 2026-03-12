from pydantic import BaseModel, Field, ConfigDict
from typing import Union, Literal
from enum import Enum

class DocumentType(str, Enum):
    SCIENTIST = "scientist"
    COMMONER = "commoner"

class ScientistContent(BaseModel):
    field: str = Field(..., description="Область науки")
    degree: str = Field(..., description="Учёная степень")
    publications: int = Field(..., description="Количество публикаций")

class ScientistDocumentCreate(BaseModel):
    type: Literal["scientist"] = Field(..., description="Тип документа")
    content: ScientistContent


class CommonerDocumentCreate(BaseModel):
    type: Literal["commoner"] = Field(..., description="Тип документа")
    content: dict = Field(..., description="Содержимое документа")


DocumentCreate = Union[
    ScientistDocumentCreate,
    CommonerDocumentCreate
]

class DocumentRead(BaseModel):
    id: int
    type: DocumentType
    content: dict
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class DocumentDiff(BaseModel):
    added: dict = Field(default_factory=dict)
    removed: dict = Field(default_factory=dict)
    changed: dict = Field(default_factory=dict)