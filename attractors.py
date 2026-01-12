from dataclasses import dataclass
from typing import Callable, Dict, List

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
    params: List[AttractorParam]
    initial_conditions: List[float]
    time_defaults: Dict[str, int]


def lorenz(x_var, t, sigma: float, rho: float, beta: float):
    x, y, z = x_var
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z

    return [dx_dt, dy_dt, dz_dt]


lorenz_attractor = AttractorConfig(
    "lorenz",
    lorenz,
    params=[
        AttractorParam("sigma", 10.0, 0.0, 50.0, 0.1),
        AttractorParam("rho", 28.0, 0.0, 50.0, 0.1),
        AttractorParam("beta", 2.67, 0.0, 50.0, 0.1),
    ],
    initial_conditions=[0.0, 1.5, 15.0],
    time_defaults={"t_min": 0, "t_max": 50, "n": 10000},
)


def rossler(x_var, t, a, b, c):
    x, y, z = x_var
    dxdt = -y - z
    dydt = x + (a * y)
    dzdt = b + z * (x - c)

    return [dxdt, dydt, dzdt]


rossler_attractor = AttractorConfig(
    "Rossler attractor",
    rossler,
    params=[
        AttractorParam("a", 0.2, 0.0, 1.0, 0.01),
        AttractorParam("b", 0.2, 0.0, 1.0, 0.01),
        AttractorParam("c", 5.7, 0.0, 20.0, 0.01),
    ],
    initial_conditions=[1.0, 1.0, 1.0],
    time_defaults={"t_min": 0, "t_max": 100, "n": 10000},
)


def dadras(x_var, t, a, b, c, d, e):
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
        AttractorParam("a", 3.0, -10.0, 10.0, 0.1),
        AttractorParam("b", 2.7, -10.0, 10.0, 0.1),
        AttractorParam("c", 1.7, -10.0, 10.0, 0.1),
        AttractorParam("d", 2.0, -10.0, 10.0, 0.1),
        AttractorParam("e", 9.0, -10.0, 10.0, 0.1),
    ],
    initial_conditions=[1.1, 2.1, -2],
    time_defaults={"t_min": 0, "t_max": 75, "n": 10000},
)

ATTRACTORS = {
    "Lorenz": lorenz_attractor,
    "Rossler": rossler_attractor,
    "Dadras": dadras_attractor,
}


def solve_attractor(config: AttractorConfig, param_values: Dict[str, float]):
    t_def = config.time_defaults
    t = np.linspace(t_def["t_min"], t_def["t_max"], t_def["n"])

    args = tuple(param_values[p.name] for p in config.params)

    solution = odeint(config.equation, config.initial_conditions, t, args=args)

    return solution


def get_default_params(config: AttractorConfig) -> Dict[str, float]:
    return {p.name: p.default for p in config.params}
