from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import Optional, List, Any
from datetime import datetime, timezone
from enum import Enum


class VariableType(str, Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    EMAIL = "email"
    NUMBER = "number"
    SELECT = "select"
    TEL = "tel"


class VariableBase(SQLModel):
    name: str = Field(description="Variable name used in templates")
    label: str = Field(description="Display label for the variable")
    type: VariableType = Field(description="Input type for the variable")
    required: bool = Field(default=False, description="Whether variable is required")
    placeholder: Optional[str] = Field(default=None, description="Placeholder text")
    default_value: Optional[str] = Field(default=None, description="Default value")
    order: int = Field(default=0, description="Display order")


class Variable(VariableBase, table=True):
    __tablename__ = "variables"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    action_id: int = Field(foreign_key="actions.id", description="Parent action ID")
    options: Optional[List[str]] = Field(default=None, sa_column=Column(JSON), description="Options for select type")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    action: "Action" = Relationship(back_populates="variables")


class VariableCreate(VariableBase):
    action_id: int
    options: Optional[List[str]] = None


class VariableRead(VariableBase):
    id: int
    action_id: int
    options: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


class VariableUpdate(SQLModel):
    name: Optional[str] = None
    label: Optional[str] = None
    type: Optional[VariableType] = None
    required: Optional[bool] = None
    placeholder: Optional[str] = None
    default_value: Optional[str] = None
    options: Optional[List[str]] = None
    order: Optional[int] = None
