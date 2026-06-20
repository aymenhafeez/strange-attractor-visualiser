from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _loop_chaotic(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = y * b
    dydt = -x - y * z
    dzdt = y**2 - a

    return [dxdt, dydt, dzdt]


loop_chaotic_attractor = AttractorConfig(
    "loop_chaotic",
    _loop_chaotic,
    params=[
        AttractorParam("$a$", 1.0, 0.0, 20.0, 0.01),
        AttractorParam("$b$", 1.796, 0.0, 10.0, 0.01),
    ],
    initial_conditions=[-0.1, -1, 0.3],
    time_defaults={"t_min": 0, "t_max": 500, "n": 10000},
    description=(
        "This is a variant of the Nosé-Hoover attractor, which was designed to \
                simulate fixed temperature molecular dynamics. It can take a wide \
                variety of unique shapes with some trajectories looking seemingly \
                random and chaotic from certain angles, but well formed and \
                deterministic from others."
    ),
    equation_text=r"$\\\dot{x}=yb,\\\dot{y}=-x-zy,\\\dot{z}=y^2-a$",
    presets={
        "Classic": {"$a$": 1.0, "$b$": 1.796},
        "Twister doughnut": {"$a$": 3.6, "$b$": 5.95},
        "Stacked attractors": {"$a$": 4.19, "$b$": 3.483},
        "Tangled chaos": {"$a$": 3.92, "$b$": 1.8},
        "Tangled chaos 2": {"$a$": 2.72, "$b$": 0.96},
    },
    prompts=[
        "Going through the parameter range of $a$ shows the attractor move from a \
                simple torus a series of weaving loops.",
        "While w$a$ dictates the shape of the system, $b$  parameterises it's scale. \
                For any given value of $a$, try different values of $b$ to see how the \
                size of the overall attractor changes",
    ],
)
