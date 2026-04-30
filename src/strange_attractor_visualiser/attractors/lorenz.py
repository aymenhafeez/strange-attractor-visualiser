from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _lorenz(
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


lorenz_attractor = AttractorConfig(
    "lorenz",
    _lorenz,
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
                wing. Lowering it much below $10$ will cause the butterfly shape to \
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
