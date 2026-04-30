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
        AttractorParam("$a$", 0.2, 0.0, 1.0, 0.001),
        AttractorParam("$b$", -0.01, -0.3, 0.15, 0.001),
        AttractorParam("$c$", 1.0, -1.0, 10.0, 0.001),
        AttractorParam("$d$", -0.4, -1.0, 0.1, 0.001),
        AttractorParam("$e$", -1.0, -5.0, 1.0, 0.001),
        AttractorParam("$f$", -1.0, -500.0, 0.0, 0.01),
    ],
    initial_conditions=[0.1, 0.1, 0.1],
    time_defaults={"t_min": 0, "t_max": 750, "n": 30000},
    description=(
        "The Wang-Sun system is a three-dimensional chaotic system that generates "
        "complex multi-wing attractors. It is characterized by its ability to "
        "produce intricate, symmetric loops that resemble a double-scroll, but "
        "with more aggressive twisting and folding along its trajectories."
    ),
    equation_text=r"$\\\dot{x}=ax+cyz,\\\dot{y}=bx+dy-xz,\\\dot{z}=ez+fxy$",
    presets={
        "Classic": {
            "$a$": 0.2,
            "$b$": -0.01,
            "$c$": 1.0,
            "$d$": -0.4,
            "$e$": -1.0,
            "$f$": -1.0,
        },
        "Spread wings": {
            "$a$": 0.8778,
            "$b$": 0.0769,
            "$c$": 8.3208,
            "$d$": -0.7024,
            "$e$": -4.3853,
            "$f$": -130.9962,
        },
        "Cone": {
            "$a$": 0.5418,
            "$b$": -0.0688,
            "$c$": 1.8342,
            "$d$": -0.6933,
            "$e$": -0.2657,
            "$f$": -465.7684,
        },
        "Spiral": {
            "$a$": 0.5091,
            "$b$": -0.0916,
            "$c$": 0.3203,
            "$d$": -0.1128,
            "$e$": -0.9546,
            "$f$": -65.2394,
        },
    },
    prompts=[
        "Adjusting $a$ and $d$ will determine if the system converges to a point or "
        "explodes into chaos.",
        "The parameter $c$ influences the strength of the coupling between the wings. "
        "Higher values tend to stretch the attractor along the x-axis.",
        "Try varying $b$; even small changes can shift the symmetry of the wings, "
        "causing one side to dominate or the entire structure to tilt.",
        "Parameters $e$ and $f$ control the vertical stability. Modifying $e$ will "
        "often 'squash' or 'elongate' the attractor along the z-axis core.",
    ],
)
