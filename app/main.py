import os
from fastapi import FastAPI, HTTPException, status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
from app.models import *
from app.schemas import *
from app.crud.authors import *
from app.crud.books import *
from sqlalchemy.exc import IntegrityError

load_dotenv(".env")
app = FastAPI(title="Biblioteca API", version="0.1.0")
app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DATABASE_URL"))

# Endpoints Autores


@app.post(
    "/authors/",
    response_model=SchemaAuthorResponse,
    status_code=status.HTTP_201_CREATED,
    description="Crea un nuevo autor en la base de datos, utilizando su nombre completo.",
    summary="Crear un autor",
)
def create_author_endpoint(author: SchemaAuthor):
    return create_author(author)


@app.get(
    "/authors/",
    response_model=list[SchemaAuthorResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los autores",
    description="Obtiene una lista de todos los autores registrados en la base de datos.",
)
def get_authors_endpoint():
    return get_authors()


@app.get(
    "/authors/{author_id}",
    response_model=SchemaAuthorResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un autor específico",
    description="Obtiene un autor específico por su ID.",
)
def get_author_endpoint(author_id: int):
    return get_author(author_id)


@app.put(
    "/authors/{author_id}",
    response_model=SchemaAuthorResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un autor",
    description="Actualiza el nombre completo de un autor específico con su ID.",
)
def update_author_endpoint(author_id: int, author: SchemaAuthor):
    return update_author(author_id, author)


@app.delete(
    "/authors/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un autor",
    description="Elimina un autor específico por su ID.",
)
def delete_author_endpoint(author_id: int):
    delete_author(author_id)


# Endpoints Libros


@app.post(
    "/books/",
    response_model=SchemaBookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un libro",
    description="Crea un nuevo libro en la base de datos, utilizando su título, ID de autor, ISBN y fecha de publicación.",
)
def create_book_endpoint(book: SchemaBook):
    return create_book(book)


@app.get(
    "/books/",
    response_model=list[SchemaBookResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los libros",
    description="Obtiene una lista de todos los libros registrados en la base de datos.",
)
def get_books_endpoint():
    return get_books()


@app.get(
    "/books/{book_id}",
    response_model=SchemaBookResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un libro específico",
    description="Obtiene un libro específico por su ID.",
)
def get_book_endpoint(book_id: int):
    return get_book(book_id)


@app.put(
    "/books/{book_id}",
    response_model=SchemaBookResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un libro",
    description="Actualiza los datos de un libro específico por su ID.",
)
def update_book_endpoint(book_id: int, book: SchemaBook):
    return update_book(book_id, book)


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un libro",
    description="Elimina un libro específico por su ID.",
)
def delete_book_endpoint(book_id: int):
    delete_book(book_id)


@app.get(
    "/books/search/",
    response_model=list[SchemaBookResponse],
    status_code=status.HTTP_200_OK,
    summary="Buscar libros",
    description="Busca libros por nombre de autor y/o año de publicación.",
)
def search_books_endpoint(author_name: str = None, year: int = None):
    return search_books(author_name, year)
