from app.models import *
from app.schemas import *
from fastapi_sqlalchemy import db
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query
from sqlalchemy import extract


def create_book(book: SchemaBook):
    """
    Crea un nuevo libro en la base de datos.

    Args:
        book (SchemaBook): Objeto que contiene los datos del libro. Debe incluir:
            title (str): Título del libro.
            author_id (int): ID del autor al que pertenece el libro.
            ISBN (str): Número de identificación único del libro.
            date_published (date): Fecha de publicación del libro.

    Returns:
        Book: El objeto del libro recién creado con su ID asignado por la base de datos.

    Raises:
        HTTPException:
            - 404: Si el autor no existe en la base de datos.
            - 400: Si ya existe un libro con el mismo ISBN.
            - 500: Si ocurre un error inesperado al intentar guardar el libro.
    """
    db_author = db.session.get(Author, book.author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = Book(
        title=book.title,
        author_id=book.author_id,
        ISBN=book.ISBN,
        date_published=book.date_published,
    )
    try:
        db.session.add(db_book)
        db.session.commit()
        return db_book
    except IntegrityError as e:
        db.session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Book already exists with ISBN: {book.ISBN}"
        )
    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating book: {str(e)}")


def get_books():
    """
    Obtiene la lista de todos los libros en la base de datos.

    Returns:
        list[Book]: Una lista de todos los libros disponibles en la base de datos.
    """
    return db.session.query(Book).all()


def get_book(book_id: int):
    """
    Obtiene un libro específico por su ID.

    Args:
        book_id (int): ID del libro a buscar.

    Returns:
        Book: El objeto del libro correspondiente al ID.

    Raises:
        HTTPException:
            - 404: Si el libro no se encuentra en la base de datos.
    """
    book = db.session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def update_book(book_id: int, book: SchemaBook):
    """
    Actualiza los datos de un libro existente en la base de datos.

    Args:
        book_id (int): ID del libro a actualizar.
        book (SchemaBook): Datos actualizados del libro. Debe incluir:
            title (str): Título del libro.
            author_id (int): ID del autor.
            ISBN (str): Número de identificación único del libro.
            date_published (date): Fecha de publicación.

    Returns:
        Book: El objeto del libro actualizado.

    Raises:
        HTTPException:
            - 404: Si el libro o el autor no existen en la base de datos.
            - 400: Si otro libro con el mismo ISBN ya existe.
            - 500: Si ocurre un error inesperado durante la actualización.
    """
    db_book = db.session.get(Book, book_id)
    db_author = db.session.get(Author, book.author_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    try:
        db_book.title = book.title
        db_book.author_id = book.author_id
        db_book.ISBN = book.ISBN
        db_book.date_published = book.date_published
        db.session.commit()
        return db_book
    except IntegrityError as e:
        db.session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Book already exists with ISBN: {book.ISBN}"
        )
    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating book: {str(e)}")


def delete_book(book_id: int):
    """
    Elimina un libro de la base de datos por su ID.

    Args:
        book_id (int): ID del libro a eliminar.

    Raises:
        HTTPException:
            - 404: Si el libro no existe en la base de datos.
            - 500: Si ocurre un error inesperado durante la eliminación.
    """
    db_book = db.session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        db.session.delete(db_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting book: {str(e)}")


def search_books(author_name: str = None, year: int = None):
    """
    Busca libros en la base de datos filtrando por nombre del autor o año de publicación.

    Args:
        author_name (str, optional): Nombre del autor (parcial o completo).
        year (int, optional): Año de publicación del libro.

    Returns:
        list[Book]: Lista de libros que coinciden con los criterios de búsqueda.

    Raises:
        HTTPException:
            - 404: Si no se encuentran libros con los criterios proporcionados.
    """
    query: Query = db.session.query(Book).join(Author)
    if author_name:
        query = query.filter(Author.full_name.ilike(f"%{author_name}%"))
    if year:
        query = query.filter(extract("year", Book.date_published) == year)

    books = query.all()

    if not books:
        raise HTTPException(
            status_code=404, detail="No books found with the given criteria"
        )

    return books
