from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# pool_pre_ping=True — перевіряє з'єднання перед кожним запитом,
# що запобігає помилкам при "stale" з'єднаннях після простою БД.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# autocommit=False — транзакції потрібно явно комітити
# autoflush=False  — зміни не скидаються автоматично перед кожним запитом
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    """
    FastAPI dependency that yields a database session and ensures
    it is properly closed after each request, even on exceptions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
