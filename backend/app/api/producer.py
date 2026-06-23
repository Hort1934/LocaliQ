from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.producer import ProducerCreate, ProducerOut, ProducerUpdate
from app.crud.producer import (
    create_producer,
    get_all_producers,
    get_producer_by_id,
    get_producers_by_category,
    update_producer,
    delete_producer,
)
from app.db.session import get_db
from app.api.auth import oauth2_scheme
from app.crud.user import get_user_by_username
from app.models.user import User
from app.config import settings
from jose import JWTError, jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    JWT dependency — validates the Bearer token and returns the current user.
    Used to protect write endpoints (POST / PUT / DELETE).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


router = APIRouter()


# ---------------------------------------------------------------------------
# Public read endpoints (no auth required)
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[ProducerOut], summary="Всі виробники")
def get_all(db: Session = Depends(get_db)):
    """Return a list of all producers sorted by name."""
    return get_all_producers(db)


@router.get("/filter/", response_model=List[ProducerOut], summary="Фільтр за категорією")
def filter_by_category(category: str, db: Session = Depends(get_db)):
    """Return producers filtered by category (case-insensitive)."""
    return get_producers_by_category(db, category)


@router.get("/{producer_id}", response_model=ProducerOut, summary="Виробник за ID")
def get_one(producer_id: int, db: Session = Depends(get_db)):
    """Return a single producer by ID."""
    producer = get_producer_by_id(db, producer_id)
    if not producer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producer with id={producer_id} not found",
        )
    return producer


# ---------------------------------------------------------------------------
# Protected write endpoints (JWT required)
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=ProducerOut,
    status_code=status.HTTP_201_CREATED,
    summary="Додати виробника",
)
def create(
    data: ProducerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new producer. Requires authentication."""
    return create_producer(db, data)


@router.put("/{producer_id}", response_model=ProducerOut, summary="Оновити виробника")
def update(
    producer_id: int,
    data: ProducerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Partially update a producer. Requires authentication."""
    producer = update_producer(db, producer_id, data)
    if not producer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producer with id={producer_id} not found",
        )
    return producer


@router.delete(
    "/{producer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити виробника",
)
def delete(
    producer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a producer. Requires authentication."""
    deleted = delete_producer(db, producer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producer with id={producer_id} not found",
        )
