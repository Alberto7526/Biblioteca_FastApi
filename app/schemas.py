from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class SchemaAuthor(BaseModel):
    full_name: str

    model_config = {
        "json_schema_extra": {"examples": [{"full_name": "Gabriel García Márquez"}]}
    }


class SchemaAuthorResponse(BaseModel):
    id: int
    full_name: str
    date_created: datetime

    model_config = ConfigDict(from_attributes=True)


class SchemaBook(BaseModel):
    title: str
    author_id: int
    ISBN: str
    date_published: date | None = None

    model_config = ConfigDict(from_attributes=True)


class SchemaBookResponse(BaseModel):
    id: int
    date_created: datetime
    title: str
    author_id: int
    ISBN: str
    date_published: date | None = None

    model_config = ConfigDict(from_attributes=True)
