"""DTO for Agent BO"""

from typing import TypedDict


class AgentDTO(TypedDict):
    """Agent DTO (Data Transfer Object)"""

    id: int
    value: float
    interval: float
    name: str
    agent_type: str
    metric_type: str
