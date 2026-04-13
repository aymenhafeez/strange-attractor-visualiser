from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class AttractorParam:
    name: str
    default: float
    min_val: float
    max_val: float
    step: float = 0.1


@dataclass
class AttractorConfig:
    name: str
    equation: Callable
    params: list[AttractorParam]
    initial_conditions: list[float]
    time_defaults: dict[str, int | float]
    description: str
    equation_text: str
    presets: dict[str, dict[str, float]]
    prompts: list[str]
