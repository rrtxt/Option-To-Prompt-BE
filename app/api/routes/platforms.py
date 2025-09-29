from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.api.deps import get_session
from app.models import Platform, PlatformRead, PlatformReadWithActions, Action, ActionRead

router = APIRouter()


@router.get("/", response_model=List[PlatformRead])
def get_platforms(
    active_only: bool = True,
    session: Session = Depends(get_session)
):
    """Get all platforms"""
    statement = select(Platform)
    if active_only:
        statement = statement.where(Platform.is_active == True)
    
    platforms = session.exec(statement).all()
    return platforms


@router.get("/{platform_id}", response_model=PlatformReadWithActions)
def get_platform(
    platform_id: int,
    session: Session = Depends(get_session)
):
    """Get platform by ID with its actions"""
    statement = select(Platform).where(Platform.id == platform_id)
    platform = session.exec(statement).first()
    
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    # Get platform actions
    actions_statement = select(Action).where(
        Action.platform_id == platform_id,
        Action.is_active == True
    )
    actions = session.exec(actions_statement).all()
    
    # Convert to response model
    platform_data = platform.model_dump()
    platform_data["actions"] = [ActionRead.model_validate(action) for action in actions]
    
    return PlatformReadWithActions.model_validate(platform_data)


@router.get("/{platform_id}/actions", response_model=List[ActionRead])
def get_platform_actions(
    platform_id: int,
    active_only: bool = True,
    session: Session = Depends(get_session)
):
    """Get all actions for a specific platform"""
    # Verify platform exists
    platform = session.exec(select(Platform).where(Platform.id == platform_id)).first()
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    # Get actions
    statement = select(Action).where(Action.platform_id == platform_id)
    if active_only:
        statement = statement.where(Action.is_active == True)
    
    actions = session.exec(statement).all()
    return actions
