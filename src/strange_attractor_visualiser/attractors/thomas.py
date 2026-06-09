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
        AttractorParam("$a$", 0.208186, 0.0, 0.4, 0.001),
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
        "Increasing the value of $a$ causes the distinct shape of the attractor to \
            unwind and spiral out.",
        "Decreasing $a$ leads to some really unique shapes. The attractor first \
            becomes a mirror of the original shape, before unravelling into some \
            really distinct spirals.",
        "The presets show some interesting shapes, however I recommend slowing \
            reducing $a$, and seeing how even changing its value by just 0.01 \
            alters its shape radically.",
    ],
)
