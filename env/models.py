from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field

class Observation(BaseModel):
    """What the agent sees at the current step."""
    script_text: str = Field(description="The current text of the Python script being refactored.")
    linter_output: str = Field(description="The raw text output from the most recent linter run.")
    current_errors: int = Field(default=0, description="Total number of active errors.")

class Action(BaseModel):
    """What the agent wants to do."""
    action_type: Literal["run_linter", "read_lines", "replace_lines", "test_execution"]
    
    # Arguments for 'run_linter'
    tool_name: Optional[str] = Field(default=None, description="'flake8' or 'mypy'")
    
    # Arguments for 'read_lines' and 'replace_lines'
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    
    # Argument for 'replace_lines'
    new_text: Optional[str] = Field(default=None, description="The new code to insert")

class Reward(BaseModel):
    """The feedback returned to the agent after an action."""
    value: float = Field(description="The numeric reward (-1.0 to 1.0) for this step.")
    done: bool = Field(description="True if the task is finished successfully or completely failed.")
    info: Dict[str, Any] = Field(default_factory=dict, description="Extra debugging info like penalties applied.")