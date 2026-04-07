from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.integrate import odeint


@dataclass
class AttractorParam:
    name: str
    default: float
    min_val: float
    max_val: float
    step: float = 0.1


@dataclass
class AttractorConfig:
    name: str
    equation: Callable
    params: list[AttractorParam]
    initial_conditions: list[float]
    time_defaults: dict[str, int]
    description: str
    equation_text: str
    presets: dict[str, dict[str, float]]
    prompts: list[str]


def lorenz(
    x_var: list[Any],
    t: int | float,
    sigma: int | float,
    rho: int | float,
    beta: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z

    return [dxdt, dydt, dzdt]


# TODO: add more attractors
lorenz_attractor = AttractorConfig(
    "lorenz",
    lorenz,
    params=[
        AttractorParam("$\\sigma$", 10.0, 0.0, 75.0, 0.01),
        AttractorParam("$\\rho$", 28.0, 0.0, 150.0, 0.01),
        AttractorParam("$\\beta$", 2.67, 0.0, 20.0, 0.01),
    ],
    initial_conditions=[0.0, 1.5, 15.0],
    time_defaults={"t_min": 0, "t_max": 50, "n": 10000},
    description=(
        "The Lorenz attractor is a set of chaotic solutions to a 3D system of \
                equations representing simplified atmospheric convection. It is famous \
                for its 'butterfly' shape, where trajectories loop infinitely around \
                two symmetric wings without ever repeating or intersecting. The Lorenz \
                attractor is the classic example of a chaotic system used to \
                demonstrate how small changes in model parameters can lead to \
                drastically different trajectories."
    ),
    equation_text=r"$\\\dot{x}=\sigma(y-x),\\\dot{y}=x(\rho-z)-y,\\\dot{z}=xy-\beta z$",
    presets={
        "Classic": {"$\\sigma$": 10.0, "$\\rho$": 28.0, "$\\beta$": 2.67},
        "Mild chaos": {"$\\sigma$": 10.0, "$\\rho$": 22.0, "$\\beta$": 2.67},
        "Stronger spread": {"$\\sigma$": 14.0, "$\\rho$": 100.0, "$\\beta$": 3.0},
    },
    prompts=[
        "Adjust $\\sigma$ to control the tightness of the spirals. Increasing it will \
                make the trajectory spiral more tightly towards the center of each \
                wing. Lowering it much below $10$ cause the butterfly shape to \
                collapse.",
        "$\\rho$ is strong driver of the chaos of the Lorenz attractor. Lower it to \
                see how the butterfly shape disappears. Increase $\\rho$ gradually and \
                watch the wings separate into a more dense pattern.",
        "Small increases to $\\beta$ eventually causes the attractor to unravel if \
                it's value is large relative to $\\rho$. Raise the value of $\\rho$ \
                first and then play with the value of $\\beta$ to compare how their \
                relative values affect the shape of the attractor.",
    ],
)


def rossler(
    x_var: list[int | float],
    t: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = -y - z
    dydt = x + (a * y)
    dzdt = b + z * (x - c)

    return [dxdt, dydt, dzdt]


rossler_attractor = AttractorConfig(
    "Rossler attractor",
    rossler,
    params=[
        AttractorParam("$a$", 0.2, 0.0, 1.0, 0.01),
        AttractorParam("$b$", 0.2, 0.0, 1.0, 0.01),
        AttractorParam("$c$", 5.7, 0.0, 20.0, 0.01),
    ],
    initial_conditions=[1.0, 1.0, 1.0],
    time_defaults={"t_min": 0, "t_max": 100, "n": 10000},
    description=(
        "The Rossler system is known for its spiral attractor and simple equations. "
        "It is a good entry point for understanding chaotic phase portraits."
    ),
    equation_text=r"$\\\dot{x}=-y-z,\\\dot{y}=x+ay,\\\dot{z}=b+z(x-c)$",
    presets={
        "Classic": {"$a$": 0.2, "$b$": 0.2, "$c$": 5.7},
        "Loose spiral": {"$a$": 0.1, "$b$": 0.1, "$c$": 8.0},
        "Tight spiral": {"$a$": 0.3, "$b$": 0.3, "$c$": 4.5},
    },
    prompts=[
        "Increase $c$ and observe how the spiral stretches.",
        "Lower $a$ and compare the orbit thickness.",
    ],
)


def dadras(
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
    dadras,
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


def three_scroll(
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
    three_scroll,
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
        "The three-scroll chaotic attractor is a 3D quadratic system that extends the "
        "classical two-wing Lorenz model by adding a third stable focal point. It "
        "consists of two symmetry-related scrolls flanking the $z$-axis and a unique "
        "third scroll that rotates directly around it. Characterised by its six "
        "parameters, this system is frequently studied in nonlinear dynamics and "
        "secure communications due to its high sensitivity to initial conditions and "
        "its complex, non-integer fractal dimension."
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


def aizawa(
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
    aizawa,
    params=[
        AttractorParam("$a$", 1.0, -0.55, 40.0, 0.01),
        AttractorParam("$b$", 0.7, -2.0, 25.0, 0.01),
        AttractorParam("$c$", 0.6, -10.0, 10.0, 0.01),
        AttractorParam("$d$", 3.5, 0.0, 500.0, 0.001),
        AttractorParam("$e$", 0.25, 0.0, 60.0, 0.01),
        AttractorParam("$f$", 0.1, -2.10, 20.0, 0.01),
    ],
    initial_conditions=[-0.29, -0.25, -0.59],
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


ATTRACTORS = {
    "Lorenz": lorenz_attractor,
    "Rossler": rossler_attractor,
    "Dadras": dadras_attractor,
    "Three-scroll": three_scroll_attractor,
    "Aizawa": aizawa_attractor,
}


def solve_attractor(
    config: AttractorConfig, param_values: dict[str, float]
) -> np.ndarray:
    t_def = config.time_defaults
    t = np.linspace(t_def["t_min"], t_def["t_max"], t_def["n"])

    args = tuple(param_values[p.name] for p in config.params)

    solution = odeint(config.equation, config.initial_conditions, t, args=args)

    return solution


def get_default_params(config: AttractorConfig) -> dict[str, float]:
    return {p.name: p.default for p in config.params}
