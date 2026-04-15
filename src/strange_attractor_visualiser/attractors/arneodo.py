from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _arneodo(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = y
    dydt = z
    dzdt = -a * x - b * y - z + c * (x**3)

    return [dxdt, dydt, dzdt]


arneodo_attractor = AttractorConfig(
    "arneodo",
    _arneodo,
    params=[
        AttractorParam("$a$", -5.5, -5.82, 2.4, 0.01),
        AttractorParam("$b$", 3.5, 3.2, 30.0, 0.01),
        AttractorParam("$c$", -1.0, -5.0, 0.1, 0.01),
    ],
    initial_conditions=[1.0, 1.0, 1.0],
    time_defaults={"t_min": 0, "t_max": 100, "n": 30000},
    description=(
        "The Arneodo attractor is a 3D chaotic system that demonstrates the \
            emergence of 'spiral chaos' through homoclinic loops. It was \
            originally introduced to explore the complex dynamics that arise \
            near certain types of mathematical bifurcations. Its trajectory \
            typically features a central spiraling core that expands and \
            contracts, creating a delicate, layered structure that appears \
            both organic and rigidly geometric."
    ),
    equation_text=r"$\\\dot{x}=y,\\\dot{y}=z,\\\dot{z}=-ax-by-z+cx^3$",
    presets={
        "Classic Spiral": {"$a$": -5.5, "$b$": 3.5, "$c$": -1.0},
    },
    prompts=[
        "Increasing $a$ strengthens the repulsion from the origin pushing the \
            trajectories outward into wider, more aggressive spirals. If it \
            is set too low, the system may settle into a simple periodic \
            orbit.",
        "Adjust $b$ to control the damping of the vertical oscillations. Higher \
            values of $b$ tend to compress the attractor along the $z$-axis, \
            leading to a flatter, more disc-like appearance, while lower \
            values allow the 'spiral' to stretch vertically.",
        "The cubic parameter $c$ introduces the essential non-linearity \
            required for chaos. Even tiny changes to $c$ can cause the \
            attractor to transition between structured ribbons and a \
            dense, cloud-like chaotic state. Watch how it affects the \
            folding of the outer layers back toward the center.",
    ],
)
