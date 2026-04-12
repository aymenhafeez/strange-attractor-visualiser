from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _three_scroll(
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
    dxdt = a * (y - x) + d * x * z
    dydt = b * x - x * z + f * y
    dzdt = c * z + x * y - e * x**2

    return [dxdt, dydt, dzdt]


three_scroll_attractor = AttractorConfig(
    "three_scroll",
    _three_scroll,
    params=[
        AttractorParam("$a$", 32.48, 0.0, 50.0, 0.01),
        AttractorParam("$b$", 71.00, 40.0, 100.0, 0.01),
        AttractorParam("$c$", 1.18, 0.0, 5.0, 0.01),
        AttractorParam("$d$", 0.13, 0.0, 1.0, 0.001),
        AttractorParam("$e$", 0.57, 0.47, 2.0, 0.001),
        AttractorParam("$f$", 14.7, 5.0, 30.0, 0.01),
    ],
    initial_conditions=[-0.29, -0.25, -0.59],
    time_defaults={"t_min": 0, "t_max": 30, "n": 30000},
    description=(
        "The three-scroll chaotic attractor is a 3D quadratic system that extends the \
            classical two-wing Lorenz model by adding a third stable focal point. It \
            consists of two symmetry-related scrolls flanking the $z$-axis and a \
            unique third scroll that rotates directly around it. Characterised by its \
            six parameters, this system is frequently studied in nonlinear dynamics \
            and secure communications due to its high sensitivity to initial \
            conditions and its complex, non-integer fractal dimension."
    ),
    equation_text=r"$\\\dot{x}=a(y-x)+dxz,\\\dot{y}=bx - xz + fy,\\\dot{z}=cz+xy-ex^2$",
    presets={
        "Classic": {
            "$a$": 32.48,
            "$b$": 71.00,
            "$c$": 1.18,
            "$d$": 0.13,
            "$e$": 0.57,
            "$f$": 14.7,
        },
        "Loose": {
            "$a$": 32.48,
            "$b$": 71.00,
            "$c$": 1.18,
            "$d$": 0.12,
            "$e$": 0.60,
            "$f$": 12.12,
        },
        "Sparse": {
            "$a$": 40.6,
            "$b$": 71.0,
            "$c$": 1.40,
            "$d$": 0.13,
            "$e$": 0.65,
            "$f$": 8.63,
        },
        "True choas": {
            "$a$": 50.0,
            "$b$": 50.0,
            "$c$": 5.0,
            "$d$": 0.15,
            "$e$": 0.70,
            "$f$": 14.70,
        },
    },
    prompts=[
        "Balance $a$ and $f$ for Stability: These parameters control the 'coupling' \
                and growth of the $x$ and $y$ planes. Increasing will pull the wings \
                closer together, while $f$ acts as an 'engine' that expands the \
                overall volume of the attractor.",
        "Use $e$ to Control the 'Z-Dip': This subtracts from the vertical growth ($z$).\
                Increasing it will squash the attractor's height and can force the \
                trajectory to stay flatter, while lowering it allows the 'scrolls' to \
                stretch higher into 3D space.",
        "Adjust $b$ to Trigger Chaos: A high $b$ value drives the rapid rotation \
                of the scrolls. Small tweaks to $b$ can cause the system to alternate \
                between a clean periodic orbit  and full chaotic turbulence.",
    ],
)
