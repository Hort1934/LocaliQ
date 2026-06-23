from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Uses the modern SQLAlchemy 2.x style (DeclarativeBase)
    instead of the deprecated sqlalchemy.ext.declarative.declarative_base().
    """
    pass
