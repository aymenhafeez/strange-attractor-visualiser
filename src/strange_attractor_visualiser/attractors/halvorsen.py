from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _halvorsen(
    x_var: list[Any],
    t: int | float,
    a: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = -a * x - 4 * y - 4 * z - y**2
    dydt = -a * y - 4 * z - 4 * x - z**2
    dzdt = -a * z - 4 * x - 4 * y - x**2

    return [dxdt, dydt, dzdt]


halvorsen_attractor = AttractorConfig(
    "halvorsen",
    _halvorsen,
    params=[
        AttractorParam("$a$", 1.35, 1.2, 6.0, 0.01),
    ],
    initial_conditions=[-1.48, -1.51, 2.04],
    time_defaults={"t_min": 0, "t_max": 75, "n": 10000},
    description=(
        "The Halvorsen attractor is a cyclic chaotic system characterized by its \
            three-fold symmetry. Unlike many other attractors that \
            center around two wings, this system produces trajectories \
            that cycle through three distinct lobes."
    ),
    equation_text=r"$\\\dot{x}=-ax-4y-4z-y^2,\\\dot{y}=-ay-4z-4x-z^2,\\\dot{z}=-az-4x-4y-x^2$",
    presets={
        "Classic": {"$a$": 1.35},
        "Simple loop": {"$a$": 1.89},
        "Outlined": {"$a$": 2.43},
    },
    prompts=[
        "The parameter $a$ acts as a damping factor that balances the system's \
            stability against its chaotic tendencies. If you lower $a$ toward $0$, \
            the trajectories will expand and the chaotic 'loops' will become \
            larger and more erratic.",
        "Increasing $a$ beyond $1.4$ typically causes the chaotic motion to \
            contract. If you raise it high enough, the attractor will \
            eventually collapse into a single stable point, losing its \
            characteristic three-lobed shape.",
        "Experiment with values of $a$ between $1.2$ and $1.4$ to find the 'sweet \
            spot' where the three lobes are most distinct. Small adjustments \
            in this range demonstrate how the system transitions from \
            ordered periodic cycles to fully developed chaos.",
    ],
)
