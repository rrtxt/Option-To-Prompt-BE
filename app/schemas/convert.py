from sqlmodel import SQLModel, Field
from typing import Dict, Any, List, Optional


class ConvertRequest(SQLModel):
    platform_id: int = Field(description="ID of the selected platform")
    action_id: int = Field(description="ID of the selected action") 
    variables: Dict[str, Any] = Field(description="User-provided variable values")


class ConvertResponse(SQLModel):
    prompt: str = Field(description="Generated prompt text")
    platform: str = Field(description="Platform name")
    action: str = Field(description="Action name")
    variables_used: Dict[str, Any] = Field(description="Variables that were used")


class ValidationError(SQLModel):
    field: str = Field(description="Field name that failed validation")
    message: str = Field(description="Validation error message")


class ErrorResponse(SQLModel):
    detail: str = Field(description="Error description")
    errors: Optional[List[ValidationError]] = Field(default=None, description="Field-specific validation errors")
