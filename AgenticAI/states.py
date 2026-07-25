# so now we are creating a graph
# first thing we need to create is a state

import os

# 1. Typed Dict
from typing import TypedDict

class State(TypedDict):
    name: str
    description: str
    transitions: dict[str, str]  # mapping of action to next state name

# 2. Pydantic Model
# it is good at type checking and data validation at runtime
from pydantic import BaseModel , field_validator
class State(BaseModel):
    topic : str
    score : int
    summary : str = ""

    @field_validator
    def score_positive(cls,v):
        if v < 0 :
            raise ValueError("Score must be positive")

# 3. Python Data Class
# but it is used very rarely
from dataclasses import dataclass, field

@dataclass
class State:
    topic : str = ""
    summary : str = ""
    message : list = field(default_factory=list)

from langgraph.graph import MessagesState

class State(MessagesState):
    user_name : str
    language : str
