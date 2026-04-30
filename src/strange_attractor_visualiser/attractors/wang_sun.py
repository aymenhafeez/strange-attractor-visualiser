from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _wang_sun(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
    d: int | float,
    e: int | float,
    f: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = a * x + c * y * z
    dydt = b * x + d * y - x * z
    dzdt = e * z + f * x * y

    return [dxdt, dydt, dzdt]


wang_sun_attractor = AttractorConfig(
    "wang_sun",
    _wang_sun,
    params=[
        AttractorParam("$a$", 0.2, -0.55, 40.0, 0.01),
        AttractorParam("$b$", -0.01, -2.0, 25.0, 0.01),
        AttractorParam("$c$", 1.0, -10.0, 10.0, 0.01),
        AttractorParam("$d$", -0.4, 0.0, 500.0, 0.001),
        AttractorParam("$e$", -1.0, 0.0, 60.0, 0.01),
        AttractorParam("$f$", -1.0, -2.10, 20.0, 0.01),
    ],
    initial_conditions=[0.1, 0.1, 0.1],
    time_defaults={"t_min": 0, "t_max": 750, "n": 30000},
    description=(
        "The wang_sun attractor differs in shape from the classic winged shape of the \
                Lorenz or Dadras attractors. Its trajectory seamingly follows the \
                surface of a sphere while twisting upwards through a funnel shaped \
                column."
    ),
    equation_text=r"$\\\dot{x}=(x-b)x-dy,\\\dot{y}=dx+(z-b)y,\\\dot{z}=c+az-\frac{z^3}{3}-(x^2+y^2)(1+ez)+fzx^3$",
    presets={
        "Classic": {
            "$a$": 1.0,
            "$b$": 0.7,
            "$c$": 0.6,
            "$d$": 3.5,
            "$e$": 0.25,
            "$f$": 0.1,
        },
        "Dense": {
            "$a$": 1.0,
            "$b$": 0.7,
            "$c$": 0.6,
            "$d$": 250.0,
            "$e$": 0.25,
            "$f$": 0.1,
        },
    },
    prompts=[
        "Reducing the value of $c$ from 0.55 to 0.54 perfectly illustrates a strange \
                attractor's sensitivity to it's parameters.",
        "The attractor's twist can be controlled with $d$. Increasing it tightens the \
                spirals around the central axis giving a more compact structure, with \
                a shell forming around the central column.",
        "Go through the range of $e$ and $f$ to see how the attractor collapses. Note \
                how when these two parameters fall out of balance it causes the \
                attractor to completely lose its structure.",
    ],
)
