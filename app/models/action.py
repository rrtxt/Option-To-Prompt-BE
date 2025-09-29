from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class ActionBase(SQLModel):
    name: str = Field(description="Display name of the action")
    slug: str = Field(index=True, description="URL-friendly identifier")
    description: Optional[str] = Field(default=None, description="Action description")
    is_active: bool = Field(default=True, description="Whether action is active")


class Action(ActionBase, table=True):
    __tablename__ = "actions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_id: int = Field(foreign_key="platforms.id", description="Parent platform ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    platform: "Platform" = Relationship(back_populates="actions")
    variables: List["Variable"] = Relationship(back_populates="action")
    template: Optional["Template"] = Relationship(back_populates="action")


class ActionCreate(ActionBase):
    platform_id: int


class ActionRead(ActionBase):
    id: int
    platform_id: int
    created_at: datetime
    updated_at: datetime


class ActionReadWithVariables(ActionRead):
    variables: List["VariableRead"] = []


class ActionReadWithTemplate(ActionRead):
    template: Optional["TemplateRead"] = None


class ActionUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

