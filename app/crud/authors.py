from app.models import *
from app.schemas import *
from sqlalchemy.exc import IntegrityError
from fastapi_sqlalchemy import db
from fastapi import HTTPException, status


def create_author(author: SchemaAuthor):
    """
    Crea un nuevo autor en la base de datos.

    Args:
        author (SchemaAuthor): Objeto con los datos del autor. Debe incluir:
            full_name (str): Nombre completo del autor.

    Returns:
        Author: El objeto del autor recién creado.

    Raises:
        HTTPException:
            - 400: Si el autor ya existe en la base de datos.
            - 500: Si ocurre un error inesperado durante la creación.
    """
    db_author = Author(full_name=author.full_name)
    try:
        db.session.add(db_author)
        db.session.commit()
        return db_author
    except IntegrityError as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=f"Author already exists")
    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating author: {str(e)}")


def get_authors():
    """
    Obtiene la lista de todos los autores en la base de datos.

    Returns:
        list[Author]: Una lista de todos los autores registrados.

    Raises:
        HTTPException:
            - 500: Si ocurre un error inesperado al obtener los autores.
    """
    try:
        authors = db.session.query(Author).all()
        return authors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching authors: {str(e)}",
        )


def get_author(author_id: int):
    """
    Obtiene un autor específico por su ID.

    Args:
        author_id (int): ID del autor a buscar.

    Returns:
        Author: El objeto del autor correspondiente al ID.

    Raises:
        HTTPException:
            - 404: Si el autor no se encuentra en la base de datos.
    """
    author = db.session.get(Author, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


def update_author(author_id: int, author: SchemaAuthor):
    """
    Actualiza los datos de un autor existente en la base de datos.

    Args:
        author_id (int): ID del autor a actualizar.
        author (SchemaAuthor): Datos actualizados del autor. Debe incluir:
            full_name (str): Nombre completo del autor.

    Returns:
        Author: El objeto del autor actualizado.

    Raises:
        HTTPException:
            - 404: Si el autor no existe en la base de datos.
            - 500: Si ocurre un error inesperado durante la actualización.
    """
    db_author = db.session.get(Author, author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    try:
        db_author.full_name = author.full_name
        db.session.commit()
        return db_author
    except Exception as e:
        db.session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating author: {str(e)}",
        )


def delete_author(author_id: int):
    """
    Elimina un autor de la base de datos por su ID.

    Args:
        author_id (int): ID del autor a eliminar.

    Raises:
        HTTPException:
            - 404: Si el autor no existe en la base de datos.
            - 500: Si ocurre un error inesperado durante la eliminación.
    """
    db_author = db.session.get(Author, author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    try:
        db.session.delete(db_author)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting author: {str(e)}",
        )
