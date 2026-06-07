from typing import Any

from ..core.models import AttractorConfig, AttractorParam


def _lorenz84(
    x_var: list[Any],
    t: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
    d: int | float,
) -> list[int | float]:
    x, y, z = x_var
    dxdt = -a * x - y**2 - z**2 + a * c
    dydt = -y + x * y - b * x * z + d
    dzdt = -z + b * x * y + x * z

    return [dxdt, dydt, dzdt]


lorenz84_attractor = AttractorConfig(
    "lorenz84",
    _lorenz84,
    params=[
        AttractorParam("$a$", 0.25, 0.0, 75.0, 0.01),
        AttractorParam("$b$", 4.0, 0.0, 150.0, 0.01),
        AttractorParam("$c$", 8.0, 0.0, 20.0, 0.01),
        AttractorParam("$d$", 1.0, 0.0, 20.0, 0.01),
    ],
    initial_conditions=[0.1, 0.0, 0.0],
    time_defaults={"t_min": 0, "t_max": 150, "n": 50000},
    description=(
        "The Lorenz84 attractor is a simplified version of the classic Lorenz attractor\
                . The Lorenz attractor was derived by Edward Lorenz in 1963 to model \
                atmospheric convection. He derived the Lorenz84 system in 1984 to \
                model the global scale flow of the atmosphere driven by the \
                temperature difference between the equator and the poles influenced by \
                the Earth's rotation."
    ),
    equation_text=r"$\\\dot{x}=-ax-y^2-z^2+ac,\\\dot{y}=-y+xy-bxz+d,\\\dot{z}=-z+bxy+xz$",
    presets={
        "Classic": {"$a$": 0.25, "$b$": 4.0, "$c$": 8.0, "$d$": 1.0},
        "Shell": {"$a$": 0.95, "$b$": 114.1, "$c$": 13.09, "$d$": 20.0},
        "Mushroom": {"$a$": 34.03, "$b$": 108.42, "$c$": 2.60, "$d$": 5.42},
    },
    prompts=[
        "Increasing $a$ _very_ gradually pulls the loops into a tight, predictable \
                orbit. Lowering it allows the system to swing freely into wider, \
                more unpredictable trajectories.",
        "Modify $b$ to control the rotation or **Coriolis** effect. High values tightly \
                twist the ribbon and force rapid, chaotic oscillations between the \
                lobes. If you lower $b$ too much, the complex 3D knot will unravel \
                into a flat, simple 2D loop.",
        "$c$ represents the driving force of the equator-to-pole temperature \
                difference. Keep it low to see the system settle into a calm, periodic \
                cycle. Raise $c$ past $6.0$ to watch the system explode into robust, \
                beautiful chaos as the jet stream becomes unstable.",
        "Adjust $d$ to change the asymmetric heating (like the contrast between land \
                and ocean). Shifting $d$ breaks the symmetry of the attractor, causing \
                one side of the chaotic ribbon to balloon outward while the other side \
                compresses into a dense knot.",
    ],
)
