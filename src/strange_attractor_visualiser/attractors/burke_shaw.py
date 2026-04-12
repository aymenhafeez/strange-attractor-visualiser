from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _burke_shaw(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = -a * (x + y)
    dydt = -y - a * x * z
    dzdt = a * x * y + b

    return [dxdt, dydt, dzdt]


burke_shaw_attractor = AttractorConfig(
    "burke_shaw",
    _burke_shaw,
    params=[
        AttractorParam("$a$", 10.0, 0.0, 30.0, 0.01),
        AttractorParam("$b$", 4.27, 0.0, 100.0, 0.01),
    ],
    initial_conditions=[0.1, 0.1, 0.1],
    time_defaults={"t_min": 0, "t_max": 100, "n": 15000},
    description=(
        "The Burke-Shaw attractor is a chaotic system derived as a variant of the \
                Lorenz equations, known for its intricate, spiraling trajectories that \
                interweave in three-dimensional space. It is highly symmetrical, being \
                invariant under a 180-degree rotation about the $z$-axis, which often \
                results in a double-wing appearance. It has a similar algebraic \
                structure to the Lorenz system, but because of it's higher topological \
                complexity, it can take a range of shapes."
    ),
    equation_text=r"$\\\dot{x}=-ax+by-yz,\\\dot{y}=x,\\\dot{z}=-z+y^2$",
    presets={
        "Classic": {"$a$": 10.0, "$b$": 4.27},
        "Loose spiral": {"$a$": 24.45, "$b$": 63.8},
        "Filled in": {"$a$": 10.0, "$b$": 50.0},
    },
    prompts=[
        "Use $a$ to scale the intensity of the spirals. Increasing or decreasing $a$ \
                doesn't necessarily affect the chaos of the system, but rather \
                moves the attractor between various well defined shapes. However, \
                increasing or decreasing past a certain point will cause it to lose \
                it's shape and either unravel or form a simple double loop.",
        "The value of $b$ controls the force of the oscillations. \
                It effectively shifts the balance of the of the attractor, \
                increasing it causes the two wings to pull apart and merge, and \
                decreasing it will cause it to eventually fall out of shape.",
    ],
)
