from pydantic import BaseModel, ConfigDict


class ProducerBase(BaseModel):
    name: str
    description: str | None = None
    category: str
    latitude: float
    longitude: float
    city: str | None = None
    contact: str | None = None


class ProducerCreate(ProducerBase):
    """Schema for creating a new producer (all required base fields)."""
    pass


class ProducerUpdate(BaseModel):
    """
    Schema for partially updating a producer.
    All fields are optional — only provided fields will be updated.
    """
    name: str | None = None
    description: str | None = None
    category: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    city: str | None = None
    contact: str | None = None


class ProducerOut(ProducerBase):
    """Schema for returning producer data in API responses."""
    id: int

    model_config = ConfigDict(from_attributes=True)
