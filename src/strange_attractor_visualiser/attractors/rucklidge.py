from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _rucklidge(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = (-a * x) + (b * y) - (y * z)
    dydt = x
    dzdt = -z + y**2

    return [dxdt, dydt, dzdt]


rucklidge_attractor = AttractorConfig(
    "rucklidge",
    _rucklidge,
    params=[
        AttractorParam("$a$", 2.0, 0.0, 30.0, 0.01),
        AttractorParam("$b$", 6.7, 0.0, 100.0, 0.01),
    ],
    initial_conditions=[1.0, 0.0, 4.5],
    time_defaults={"t_min": 0, "t_max": 150, "n": 10000},
    description=(
        "The Rucklidge attractor arises from a simplified model of double-diffusive \
                convection, specifically describing the motion of a fluid in a \
                rotating box heated from below. Unlike the sprawling wings of the \
                Lorenz system, the Rucklidge attractor is known for its distinct, \
                'folded' structure that resembles a thin, curved ribbon or a chaotic \
                wave. It captures the transition from steady convection to complex, \
                non-periodic oscillations, serving as a quintessential example of how \
                symmetry-breaking in fluid dynamics can lead to elegant, yet \
                unpredictable, geometric forms."
    ),
    equation_text=r"$\\\dot{x}=-ax+by-yz,\\\dot{y}=x,\\\dot{z}=-z+y^2$",
    presets={
        "Classic": {"$a$": 2.0, "$b$": 6.7},
        "Wide spread": {"$a$": 4.5, "$b$": 26.72},
        "Spiral center": {"$a$": 2.0, "$b$": 47.5},
    },
    prompts=[
        "$a$ controls the spread of the spirals. Lowering its value will tighten the \
                loops, while increasing it will cause the spirals to spread and \
                eventually unravel",
        "$b$ is the main driver of the chaos in the Rucklidge attractor. Lowering it \
                causes it phase in and out of different forms of the same shape before \
                loosing form completely into a single point. However, increasing $b$ \
                causes moves the system away from its winged shape and the wings being \
                to wrap around the center.",
    ],
)
