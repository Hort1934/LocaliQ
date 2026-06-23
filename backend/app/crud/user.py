from sqlalchemy.orm import Session
import bcrypt

from app.models.user import User
from app.schemas.user import UserCreate


def get_password_hash(password: str) -> str:
    """Return bcrypt hash of the given plain-text password."""
    # Convert string to bytes, hash it, then decode back to a string for DB storage
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    # checkpw expects both values to be in bytes
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )


def get_user_by_username(db: Session, username: str) -> User | None:
    """Lookup a user by username. Returns None if not found."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Lookup a user by email address. Returns None if not found."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Lookup a user by primary key. Returns None if not found."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user with a hashed password.
    Raises nothing — caller is responsible for checking uniqueness beforehand.
    """
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user