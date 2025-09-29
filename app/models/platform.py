from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class PlatformBase(SQLModel):
    name: str = Field(index=True, description="Display name of the platform")
    slug: str = Field(unique=True, index=True, description="URL-friendly identifier")
    description: Optional[str] = Field(default=None, description="Platform description")
    is_active: bool = Field(default=True, description="Whether platform is active")


class Platform(PlatformBase, table=True):
    __tablename__ = "platforms"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    actions: List["Action"] = Relationship(back_populates="platform")


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: int
    created_at: datetime
    updated_at: datetime


class PlatformReadWithActions(PlatformRead):
    actions: List["ActionRead"] = []


class PlatformUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
