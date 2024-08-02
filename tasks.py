from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    id_task: int = 0
    offset: int = 0
    computation_time: int = 0
    period_time: int = 0
    quantum: int = 0
    deadline: int = 0

@dataclass
class ScheduleConfig:
    simulation_time: int = 0
    scheduler_name: str = ""
    tasks_number: int = 0
    tasks: List[Task] = field(default_factory=list)

