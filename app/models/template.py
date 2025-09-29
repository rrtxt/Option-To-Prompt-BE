from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone


class TemplateBase(SQLModel):
    content: str = Field(description="Template content with placeholders")
    is_active: bool = Field(default=True, description="Whether template is active")


class Template(TemplateBase, table=True):
    __tablename__ = "templates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    action_id: int = Field(foreign_key="actions.id", unique=True, description="Associated action ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    action: "Action" = Relationship(back_populates="template")


class TemplateCreate(TemplateBase):
    action_id: int


class TemplateRead(TemplateBase):
    id: int
    action_id: int
    created_at: datetime
    updated_at: datetime


class TemplateUpdate(SQLModel):
    content: Optional[str] = None
    is_active: Optional[bool] = None
