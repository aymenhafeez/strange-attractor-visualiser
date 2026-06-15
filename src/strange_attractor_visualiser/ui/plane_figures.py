import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_PALETTE = {"face": "none", "scatter": "#eeeeee", "label": "#888888"}


def _make_plane(x: np.ndarray, y: np.ndarray, label: str) -> np.ndarray:
    fig, ax = plt.subplots(figsize=(180 / 80, 100 / 80), dpi=80)
    ax.scatter(
        x[:5000], y[:5000], s=0.5, c=_PALETTE["scatter"], alpha=0.7, linewidths=0
    )

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


def x_y_plane(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return _make_plane(x, y, "x-y")


def x_z_plane(x: np.ndarray, z: np.ndarray) -> np.ndarray:
    return _make_plane(x, z, "x-z")


def y_z_plane(y: np.ndarray, z: np.ndarray) -> np.ndarray:
    return _make_plane(y, z, "y-z")
