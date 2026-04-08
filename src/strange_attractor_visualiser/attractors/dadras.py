from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _dadras(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
    d: int | float,
    e: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = y - a * x + b * y * z
    dydt = c * y - x * z + z
    dzdt = d * x * y - e * z

    return [dxdt, dydt, dzdt]


# x_solve = solve_dadras(init_cond, t, a=3, b=2.7, c=1.7, d=2, e=9)

dadras_attractor = AttractorConfig(
    "Dadras attractor",
    _dadras,
    params=[
        AttractorParam("$a$", 3.0, 0.0, 10.0, 0.1),
        AttractorParam("$b$", 2.7, 0.0, 30.0, 0.1),
        AttractorParam("$c$", 1.7, 0.0, 7.40, 0.1),
        AttractorParam("$d$", 2.0, 0.0, 15.0, 0.1),
        AttractorParam("$e$", 9.0, 0.0, 15.0, 0.1),
    ],
    initial_conditions=[1.1, 2.1, -2],
    time_defaults={"t_min": 0, "t_max": 75, "n": 10000},
    description=(
        "The Dadras system is known for it's multiwing shape. Unlike the Lorenz \
                attractor, the Dadras attractor forms a more compact volume, spiraling \
                around a central core with the wings spreading out around it."
    ),
    equation_text=r"$\\\dot{x}=y-ax+byz,\\\dot{y}=cy-xz+z,\\\dot{z}=dxy-ez$",
    presets={
        "Classic": {"$a$": 3.0, "$b$": 2.7, "$c$": 1.7, "$d$": 2.0, "$e$": 9.0},
        "Softer": {"$a$": 2.0, "$b$": 1.5, "$c$": 1.2, "$d$": 1.5, "$e$": 6.0},
        "Butterfly": {"$a$": 3.0, "$b$": 2.7, "$c$": 3.6, "$d$": 0.2, "$e$": 9.0},
        "Hollow center": {"$a$": 3.2, "$b$": 10.6, "$c$": 1.7, "$d$": 2.9, "$e$": 5.2},
    },
    prompts=[
        "$a$ controls the inflation of the attractor. Increase to see how the shape \
                unravels, or lower it expand it out into a wider structure.",
        "Try different combinations of $b$ and $c$. These control the scroll \
                complexity and increasing them will add more layers to the attractor's \
                surface.",
        "Balancing the value of $d$ controls the stability of the scroll shape. \
                Increasing it will cause the system to transition in and out of a \
                stable structure, before eventually completely unravelling.",
        "Making small changes to $e$ will show the attractor snap between order and \
                chaos.",
    ],
)
