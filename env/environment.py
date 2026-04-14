from typing import Tuple, Dict, Any
from env.models import Observation, Action, Reward

class CleanCodeEnv:
    def __init__(self):
        # internal state of the environment 
        self.current_task = None
        self.script_lines = []
        self.last_linter_output = ""
        self.step_count = 0

    def reset(self, task_id: str = "easy") -> Observation:
        """Resets the environment for a new task."""
        self.current_task = task_id
        self.step_count = 0
        
        # TODO load the bad .py file from the tasks/ folder
        self.script_lines = ["def foo(items=[]):", "    print(items)"]
        self.last_linter_output = "No linter run yet."
        
        return Observation(
            script_text="\n".join(self.script_lines),
            linter_output=self.last_linter_output,
            current_errors=1 # Dummy value for now
        )
    
    def step(self, action: Action) -> Tuple[Observation, Reward]:
        """Applies the agent's action and returns the new state and reward."""
        self.step_count += 1
        
        # TODO : Implement actual subprocess calls to linters and string replacement
        if action.action_type == "run_linter":
            self.last_linter_output = f"Simulated {action.tool_name} output: 0 errors."
            is_done = True
        else:
            is_done = False

        obs = Observation(
            script_text="\n".join(self.script_lines),
            linter_output=self.last_linter_output,
            current_errors=0 if is_done else 1
        )
        
        reward = Reward(
            value=1.0 if is_done else -0.01, # Small penalty per step, 1.0 for finishing
            done=is_done,
            info={"step_count": self.step_count}
        )
        
        return obs, reward
    
    def state(self) -> Dict[str, Any]:
        """return raw internal state of the environment."""
        return {
            "current_task": self.current_task,
            "step_count": self.step_count,
            "script_length": len(self.script_lines)
        }