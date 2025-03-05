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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "date_created": "2021-08-02T00:00:00",
                    "full_name": "Gabriel García Márquez",
                }
            ]
        }
    }


class SchemaBook(BaseModel):
    title: str
    author_id: int
    ISBN: str
    date_published: date | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Cien años de soledad",
                    "author_id": 1,
                    "ISBN": "978-3-16-148410-0",
                    "date_published": "1967-05-30",
                }
            ]
        }
    }


class SchemaBookResponse(BaseModel):
    id: int
    date_created: datetime
    title: str
    author_id: int
    ISBN: str
    date_published: date | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "date_created": "2021-08-02T00:00:00",
                    "title": "Cien años de soledad",
                    "author_id": 1,
                    "ISBN": "978-3-16-148410-0",
                    "date_published": "1967-05-30",
                }
            ]
        }
    }
