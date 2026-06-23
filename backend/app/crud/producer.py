from sqlalchemy.orm import Session
from app.models.producer import Producer
from app.schemas.producer import ProducerCreate, ProducerUpdate


def create_producer(db: Session, data: ProducerCreate) -> Producer:
    """Create and persist a new Producer record."""
    producer = Producer(**data.model_dump())
    db.add(producer)
    db.commit()
    db.refresh(producer)
    return producer


def get_all_producers(db: Session) -> list[Producer]:
    """Return all producers ordered by name."""
    return db.query(Producer).order_by(Producer.name).all()


def get_producer_by_id(db: Session, producer_id: int) -> Producer | None:
    """Return a single producer by primary key, or None if not found."""
    return db.query(Producer).filter(Producer.id == producer_id).first()


def get_producers_by_category(db: Session, category: str) -> list[Producer]:
    """Return all producers that match the given category (case-insensitive)."""
    return (
        db.query(Producer)
        .filter(Producer.category.ilike(category))
        .order_by(Producer.name)
        .all()
    )


def update_producer(
    db: Session, producer_id: int, data: ProducerUpdate
) -> Producer | None:
    """
    Partially update a producer.
    Only fields explicitly set in the request body are updated (exclude_unset).
    Returns None if the producer does not exist.
    """
    producer = get_producer_by_id(db, producer_id)
    if not producer:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(producer, field, value)
    db.commit()
    db.refresh(producer)
    return producer


def delete_producer(db: Session, producer_id: int) -> bool:
    """
    Delete a producer by id.
    Returns True on success, False if the producer was not found.
    """
    producer = get_producer_by_id(db, producer_id)
    if not producer:
        return False
    db.delete(producer)
    db.commit()
    return True
