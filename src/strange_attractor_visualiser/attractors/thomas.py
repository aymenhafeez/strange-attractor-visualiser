from typing import Any

import numpy as np

from ..core.models import AttractorConfig, AttractorParam


def _thomas(
    x_var: list[Any],
    t: int | float,
    a: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = np.sin(y) - a * x
    dydt = np.sin(z) - a * y
    dzdt = np.sin(x) - a * z

    return [dxdt, dydt, dzdt]


thomas_attractor = AttractorConfig(
    "thomas",
    _thomas,
    params=[
        AttractorParam("$a$", 0.208186, 0.0, 0.23, 0.001),
    ],
    initial_conditions=[1.1, 1.1, -0.01],
    time_defaults={"t_min": 0, "t_max": 500, "n": 10000},
    description=(
        "The Thomas attractor is a three dimensional chaotic system that \
            generates a highly symmetric, labyrinth-like lattice structure. Unlike \
            traditional butterfly shaped attractors, it uses simple trigonometric \
            functions to drive trajectories through an ordered grid of chaos, \
            resembling a complex, infinitely looping geometric cage."
    ),
    equation_text=r"$\\\dot{x}=-ax+by-yz,\\\dot{y}=x,\\\dot{z}=-z+y^2$",
    presets={
        "Classic": {"$a$": 0.208186},
        "Symmetry": {"$a$": 0.185},
        "Chaos": {"$a$": 0.078},
    },
    prompts=[
        "Because the Thomas attractor is only stable over a short range of values of \
                $a$, use the 'Random' button to see the broad variety of shapes this \
                relatively simple system can take"
    ],
)
