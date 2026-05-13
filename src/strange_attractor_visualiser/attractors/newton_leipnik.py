from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _newton_leipnik(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = -a * x + y + 10 * y * z
    dydt = -x - 0.4 * y + 5 * x * z
    dzdt = b * z - 5 * x * y

    return [dxdt, dydt, dzdt]


newton_leipnik_attractor = AttractorConfig(
    "newton_leipnik attractor",
    _newton_leipnik,
    params=[
        AttractorParam("$a$", 0.4, -4.0, 10.0, 0.01),
        AttractorParam("$b$", 0.175, -3.0, 3.0, 0.01),
    ],
    initial_conditions=[0.349, 0.0, -0.16],
    time_defaults={"t_min": 0, "t_max": 250, "n": 10000},
    description=(
        "The Newton-Leipnik system is characterized by its dual-lobed structure, "
        "often appearing as two symmetrical, spiraling leaves. It is unique for "
        "exhibiting bi-stability, where two different chaotic trajectories can "
        "co-exist within the same space."
    ),
    equation_text=r"$\\\dot{x}=-ax + y + 10xz,\\\dot{y}=-x-0.4y+5xz,\\\dot{z}=bz-5xy$",
    presets={
        "Classic": {"$a$": 0.4, "$b$": 0.175},
        "Tight Spiral": {"$a$": 0.42, "$b$": 0.15},
        "Loose Chaos": {"$a$": 0.38, "$b$": 0.2},
        "Symmetry Break": {"$a$": 0.45, "$b$": 0.12},
    },
    prompts=[
        "$a$ acts as the primary dissipation factor. Increase it to see the \
                attractor contract inward, or lower it to watch the leaves expand \
                and become more chaotic.",
        "Adjusting $b$ modifies the non-linear coupling. Increasing this \
                value adds more layers to the visual thickness of the attractor by \
                increasing the complexity of the spirals.",
        "The interaction between $a$ and $b$ is delicate in that making small changes \
                will show the system transition between a stable double-spiral and \
                completely unravelling into infinity.",
    ],
)
