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
        "The double_scroll attractor is a set of chaotic solutions to a 3D system of \
                equations modelling simplified atmospheric convection. It is famous \
                for its 'butterfly' shape, where trajectories loop infinitely around \
                two symmetric wings without ever repeating or intersecting. The double_scroll \
                attractor is the classic example of a chaotic system used to \
                demonstrate how small changes in model parameters can lead to \
                drastically different trajectories."
    ),
    equation_text=r"$\\\dot{x}=a(y-x),\\\dot{y}=x(b-z)-y,\\\dot{z}=xy-c z$",
    presets={
        "Classic": {"$a$": 0.1, "$b$": 0.497},
        "Smooth": {"$a$": 0.25, "$b$": 1.0},
        "Spread out": {"$a$": 1.54, "$b$": 0.95},
        "Six wing": {"$a$": 0.11, "$b$": 0.779},
    },
    prompts=[
        "$a$ controls the spread of the wings. Increasing it's value causes the two \
                spirals to spread and eventually form two distinct loops.",
        "The value of $b$ controls the balance of the density between the two lobes. \
                Beyond $b=1$ the system looses its shape and collapses into a single \
                loop.",
        "The attractor is stable in only short range of each parameter, but certain \
                pairings of $a$ and $b$ lead to some interesting trajectories.",
    ],
)
