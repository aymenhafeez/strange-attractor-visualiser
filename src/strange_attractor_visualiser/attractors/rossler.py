from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _rossler(
    x_var: list[int | float],
    t: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = -y - z
    dydt = x + (a * y)
    dzdt = b + z * (x - c)

    return [dxdt, dydt, dzdt]


rossler_attractor = AttractorConfig(
    "Rossler attractor",
    _rossler,
    params=[
        AttractorParam("$a$", 0.2, 0.0, 0.4, 0.01),
        AttractorParam("$b$", 0.2, 0.0, 1.0, 0.01),
        AttractorParam("$c$", 5.7, 0.0, 20.0, 0.01),
    ],
    initial_conditions=[1.0, 1.0, 1.0],
    time_defaults={"t_min": 0, "t_max": 100, "n": 10000},
    description=(
        "The Rossler attractor is one of the simplest choatic systems. It exhibits a \
                flat spiral with trajectories looping over the flat plane."
    ),
    equation_text=r"$\\\dot{x}=-y-z,\\\dot{y}=x+ay,\\\dot{z}=b+z(x-c)$",
    presets={
        "Classic": {"$a$": 0.2, "$b$": 0.2, "$c$": 5.7},
        "Loose spiral": {"$a$": 0.1, "$b$": 0.1, "$c$": 8.0},
        "Tight spiral": {"$a$": 0.37, "$b$": 0.73, "$c$": 5.7},
        "Wide multi-loop": {"$a$": 0.37, "$b$": 0.73, "$c$": 19.5},
    },
    prompts=[
        "Increasing $c$ from $0$ upwards shows the attractor going from a flat spiral \
                to the attractor looping over itself.",
        "$a$ controls how the loop of the attractor expands above the spiral. Reducing \
                its value causes the spiral to spread and the loop to shorten, while \
                increasing it will do the opposite.",
        "$b$ determines how the trajectory re-enters the main spiral. Tweaking this \
                value can change how densely the lines pack together on the flat part \
                of the ribbon.",
    ],
)
