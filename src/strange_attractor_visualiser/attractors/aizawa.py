from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _aizawa(
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
    dxdt = (z - b) * x - d * y
    dydt = d * x + (z - b) * y
    dzdt = c + a * z - (z**3 / 3) - (x**2 + y**2) * (1 + e * z) + (f * z * x**3)

    return [dxdt, dydt, dzdt]


aizawa_attractor = AttractorConfig(
    "aizawa",
    _aizawa,
    params=[
        AttractorParam("$a$", 0.95, -0.55, 40.0, 0.01),
        AttractorParam("$b$", 0.7, -2.0, 25.0, 0.01),
        AttractorParam("$c$", 0.6, -10.0, 10.0, 0.01),
        AttractorParam("$d$", 3.5, 0.0, 500.0, 0.001),
        AttractorParam("$e$", 0.25, 0.0, 60.0, 0.01),
        AttractorParam("$f$", 0.1, -2.10, 20.0, 0.01),
    ],
    initial_conditions=[0.1, 0.0, 0.0],
    time_defaults={"t_min": 0, "t_max": 30, "n": 30000},
    description=(
        "The Aizawa attractor differs in shape from the classic winged shape of the \
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
