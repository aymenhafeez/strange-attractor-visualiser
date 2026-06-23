import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .figure import DISPLAY_MODE_LINES, DISPLAY_MODE_LINES_POINTS

_PALETTE = {
    "face": "none",
    "scatter": "#eeeeee",
    "line": "#eeeeee",
    "label": "#888888",
}


def _draw_plane_points(ax, x: np.ndarray, y: np.ndarray, display_mode: str) -> None:
    if display_mode in (DISPLAY_MODE_LINES, DISPLAY_MODE_LINES_POINTS):
        ax.plot(x[:5000], y[:5000], c=_PALETTE["line"], alpha=0.55, linewidth=0.45)

    if display_mode != DISPLAY_MODE_LINES:
        ax.scatter(
            x[:5000],
            y[:5000],
            s=0.5,
            c=_PALETTE["scatter"],
            alpha=0.7,
            linewidths=0,
        )


def _make_plane(
    x: np.ndarray, y: np.ndarray, label: str, display_mode: str
) -> np.ndarray:
    fig, ax = plt.subplots(figsize=(180 / 80, 100 / 80), dpi=80)
    _draw_plane_points(ax, x, y, display_mode)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(which="both", length=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(_PALETTE["face"])
    fig.patch.set_facecolor(_PALETTE["face"])
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.text(
        0.0,
        1.0,
        label,
        transform=ax.transAxes,
        fontsize=7,
        color=_PALETTE["label"],
        fontfamily="monospace",
        va="top",
        fontweight="bold",
    )
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)

    return buf


def x_y_plane(x: np.ndarray, y: np.ndarray, display_mode: str) -> np.ndarray:
    return _make_plane(x, y, "x-y", display_mode)


def x_z_plane(x: np.ndarray, z: np.ndarray, display_mode: str) -> np.ndarray:
    return _make_plane(x, z, "x-z", display_mode)


def y_z_plane(y: np.ndarray, z: np.ndarray, display_mode: str) -> np.ndarray:
    return _make_plane(y, z, "y-z", display_mode)
