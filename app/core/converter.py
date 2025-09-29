from typing import Dict, Any, List
from jinja2 import Template as Jinja2Template, TemplateError
from app.models import Template, Variable, Action, Platform
from app.schemas.convert import ValidationError
from sqlmodel import Session, select


class PromptConverter:
    """Core prompt conversion logic"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def convert_to_prompt(
        self, 
        platform_id: int, 
        action_id: int, 
        variables: Dict[str, Any]
    ) -> tuple[str, List[ValidationError]]:
        """
        Convert platform + action + variables to final prompt
        
        Returns:
            tuple: (generated_prompt, validation_errors)
        """
        # Validate the combination exists
        action = self._get_action(platform_id, action_id)
        if not action:
            return "", [ValidationError(field="action", message="Invalid platform/action combination")]
        
        # Get template
        template = self._get_template(action_id)
        if not template:
            return "", [ValidationError(field="template", message="No template found for this action")]
        
        # Get variables definition
        variable_defs = self._get_variables(action_id)
        
        # Validate variables
        validation_errors = self._validate_variables(variable_defs, variables)
        if validation_errors:
            return "", validation_errors
        
        # Generate prompt
        try:
            prompt = self._generate_prompt(template.content, variables)
            return prompt, []
        except Exception as e:
            return "", [ValidationError(field="template", message=f"Template error: {str(e)}")]
    
    def _get_action(self, platform_id: int, action_id: int) -> Action | None:
        """Get action and verify it belongs to the platform"""
        statement = select(Action).where(
            Action.id == action_id,
            Action.platform_id == platform_id,
            Action.is_active == True
        )
        return self.session.exec(statement).first()
    
    def _get_template(self, action_id: int) -> Template | None:
        """Get template for action"""
        statement = select(Template).where(
            Template.action_id == action_id,
            Template.is_active == True
        )
        return self.session.exec(statement).first()
    
    def _get_variables(self, action_id: int) -> List[Variable]:
        """Get variable definitions for action"""
        statement = select(Variable).where(Variable.action_id == action_id)
        return list(self.session.exec(statement).all())
    
    def _validate_variables(
        self, 
        variable_defs: List[Variable], 
        user_variables: Dict[str, Any]
    ) -> List[ValidationError]:
        """Validate user variables against definitions"""
        errors = []
        
        for var_def in variable_defs:
            value = user_variables.get(var_def.name)
            
            # Check required fields
            if var_def.required and (value is None or str(value).strip() == ""):
                errors.append(ValidationError(
                    field=var_def.name,
                    message=f"{var_def.label} is required"
                ))
                continue
            
            # Validate select options
            if var_def.type == "select" and var_def.options and value:
                if str(value) not in var_def.options:
                    errors.append(ValidationError(
                        field=var_def.name,
                        message=f"{var_def.label} must be one of: {', '.join(var_def.options)}"
                    ))
            
            # Validate email format (basic)
            if var_def.type == "email" and value:
                if "@" not in str(value):
                    errors.append(ValidationError(
                        field=var_def.name,
                        message=f"{var_def.label} must be a valid email address"
                    ))
            
            # Validate number format
            if var_def.type == "number" and value is not None:
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors.append(ValidationError(
                        field=var_def.name,
                        message=f"{var_def.label} must be a valid number"
                    ))
        
        return errors
    
    def _generate_prompt(self, template_content: str, variables: Dict[str, Any]) -> str:
        """Generate prompt from template and variables with Browser Use optimizations"""
        try:
            # Use Jinja2 for advanced template processing
            template = Jinja2Template(template_content)
            
            # Filter out None values and convert to strings
            clean_variables = {
                k: str(v) if v is not None else ""
                for k, v in variables.items()
            }
            
            # Add Browser Use specific context if not already present
            rendered_prompt = template.render(**clean_variables)
            
            # Enhance prompt with Browser Use best practices
            enhanced_prompt = self._enhance_for_browser_use(rendered_prompt)
            
            return enhanced_prompt.strip()
            
        except TemplateError as e:
            raise Exception(f"Template rendering error: {str(e)}")
        except Exception as e:
            raise Exception(f"Prompt generation error: {str(e)}")
    
    def _enhance_for_browser_use(self, prompt: str) -> str:
        """Enhance prompt with Browser Use specific patterns"""
        # Check if prompt already follows Browser Use patterns
        if "You are a web automation agent" in prompt:
            # Already enhanced, return as-is
            return prompt
        
        # Add Browser Use context wrapper for legacy templates
        enhanced = f"""You are a web automation agent. Your task is to execute the following action using browser automation:

{prompt}

Instructions for execution:
1. Take your time to understand the current page state
2. Look for the most reliable selectors (prefer IDs, then classes, then text content)
3. Handle dynamic content and loading states appropriately  
4. Provide clear feedback on what you're doing at each step
5. If elements are not immediately visible, try scrolling or waiting briefly
6. Report any errors encountered with specific details

Success criteria: Complete the requested action accurately and confirm the result."""
        
        return enhanced
