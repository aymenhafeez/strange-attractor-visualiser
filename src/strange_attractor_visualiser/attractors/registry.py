from ..attractors.aizawa import aizawa_attractor
from ..attractors.dadras import dadras_attractor
from ..attractors.lorenz import lorenz_attractor
from ..attractors.rossler import rossler_attractor
from ..attractors.three_scroll import three_scroll_attractor

ATTRACTORS = {
    "Lorenz": lorenz_attractor,
    "Rossler": rossler_attractor,
    "Dadras": dadras_attractor,
    "Three-scroll": three_scroll_attractor,
    "Aizawa": aizawa_attractor,
}
