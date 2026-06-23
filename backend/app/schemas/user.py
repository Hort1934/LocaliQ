from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """Schema for registering a new user."""
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Schema for returning user data in API responses."""
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for the JWT token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for decoded JWT token payload."""
    username: str | None = None
