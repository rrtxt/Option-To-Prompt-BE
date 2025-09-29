from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.api.deps import get_session
from app.models import Action, ActionRead, ActionReadWithVariables, Variable, VariableRead

router = APIRouter()


@router.get("/{action_id}", response_model=ActionReadWithVariables)
def get_action(
    action_id: int,
    session: Session = Depends(get_session)
):
    """Get action by ID with its variables"""
    statement = select(Action).where(Action.id == action_id)
    action = session.exec(statement).first()
    
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    # Get action variables
    variables_statement = select(Variable).where(Variable.action_id == action_id).order_by(Variable.order)
    variables = session.exec(variables_statement).all()
    
    # Convert to response model
    action_data = action.model_dump()
    action_data["variables"] = [VariableRead.model_validate(var) for var in variables]
    
    return ActionReadWithVariables.model_validate(action_data)


@router.get("/{action_id}/variables", response_model=List[VariableRead])
def get_action_variables(
    action_id: int,
    session: Session = Depends(get_session)
):
    """Get all variables for a specific action"""
    # Verify action exists
    action = session.exec(select(Action).where(Action.id == action_id)).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    # Get variables ordered by display order
    statement = select(Variable).where(Variable.action_id == action_id).order_by(Variable.order)
    variables = session.exec(statement).all()
    return variables
