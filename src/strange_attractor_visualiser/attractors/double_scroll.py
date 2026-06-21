from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _double_scroll(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = y - 2 * x * z
    dydt = -x + 0.5 * (1 - x**2) * y - 0.5 * y * z
    dzdt = 0.1 * x * y + a * x**2 - 0.8 * b

    return [dxdt, dydt, dzdt]


double_scroll_attractor = AttractorConfig(
    "double_scroll",
    _double_scroll,
    params=[
        AttractorParam("$a$", 0.1, 0.0, 5.0, 0.01),
        AttractorParam("$b$", 0.5, 0.0, 5.0, 0.01),
    ],
    initial_conditions=[0.1, 2, 0.1],
    time_defaults={"t_min": 0, "t_max": 500, "n": 8000},
    description=(
        "Qiu et al. derived this attractor as a variant of the Sprott A system, with \
                the addition of cubic nonlinear term in order to construct a novel 3D \
                chaotic circuit method. While the system has the classic two wings \
                shown by other attractors, what's unique is that the wings intertwine \
                and loop into two other downward facing lobes, before looping back up."
    ),
    equation_text=r"$\\\dot{x}=a(y-x),\\\dot{y}=x(b-z)-y,\\\dot{z}=xy-c z$",
    presets={
        "Classic": {"$a$": 0.1, "$b$": 0.497},
        "Smooth": {"$a$": 0.25, "$b$": 1.0},
        "Spread out": {"$a$": 1.54, "$b$": 0.95},
        "Six wing": {"$a$": 0.11, "$b$": 0.779},
    },
    prompts=[
        "$a$ controls how much the attractor gets stretched in the $z$ direction. \
                Increasing it's value causes the two spirals to spread and eventually \
                form two distinct loops being pulled upwards.",
        "The value of $b$ controls the balance of the density between the two lobes. \
                Beyond $b=1$ the system looses its shape and collapses into a single \
                loop.",
        "The attractor is stable in only a short range of each values, but certain \
                pairings of $a$ and $b$ lead to some interesting trajectories.",
    ],
)
