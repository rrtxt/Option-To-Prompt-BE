from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_session
from app.core.converter import PromptConverter
from app.schemas.convert import ConvertRequest, ConvertResponse, ErrorResponse
from app.models import Platform, Action

router = APIRouter()


@router.post("/", response_model=ConvertResponse)
def convert_to_prompt(
    request: ConvertRequest,
    session: Session = Depends(get_session)
):
    """
    Convert platform + action + variables to a final prompt
    """
    # Initialize converter
    converter = PromptConverter(session)
    
    # Get platform and action names for response
    platform = session.exec(select(Platform).where(Platform.id == request.platform_id)).first()
    action = session.exec(select(Action).where(Action.id == request.action_id)).first()
    
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    # Convert to prompt
    prompt, validation_errors = converter.convert_to_prompt(
        request.platform_id,
        request.action_id, 
        request.variables
    )
    
    # Handle validation errors
    if validation_errors:
        raise HTTPException(
            status_code=422,
            detail=ErrorResponse(
                detail="Validation failed",
                errors=validation_errors
            ).model_dump()
        )
    
    # Return successful response
    return ConvertResponse(
        prompt=prompt,
        platform=platform.name,
        action=action.name,
        variables_used=request.variables
    )


@router.post("/validate")
def validate_variables(
    request: ConvertRequest,
    session: Session = Depends(get_session)
):
    """
    Validate variables without generating prompt
    """
    converter = PromptConverter(session)
    
    # Just run validation
    _, validation_errors = converter.convert_to_prompt(
        request.platform_id,
        request.action_id,
        request.variables
    )
    
    if validation_errors:
        return {
            "valid": False,
            "errors": [error.model_dump() for error in validation_errors]
        }
    
    return {"valid": True, "errors": []}
