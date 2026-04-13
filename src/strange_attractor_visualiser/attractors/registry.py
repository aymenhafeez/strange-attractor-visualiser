from ..attractors.aizawa import aizawa_attractor
from ..attractors.arneodo import arneodo_attractor
from ..attractors.burke_shaw import burke_shaw_attractor
from ..attractors.dadras import dadras_attractor
from ..attractors.halvorsen import halvorsen_attractor
from ..attractors.lorenz import lorenz_attractor
from ..attractors.rossler import rossler_attractor
from ..attractors.rucklidge import rucklidge_attractor
from ..attractors.three_scroll import three_scroll_attractor

ATTRACTORS = {
    "Lorenz": lorenz_attractor,
    "Rossler": rossler_attractor,
    "Dadras": dadras_attractor,
    "Three-scroll": three_scroll_attractor,
    "Aizawa": aizawa_attractor,
    "Rucklidge": rucklidge_attractor,
    "Burke-shaw": burke_shaw_attractor,
    "Arneoda": arneodo_attractor,
    "Halvorsen": halvorsen_attractor,
}
