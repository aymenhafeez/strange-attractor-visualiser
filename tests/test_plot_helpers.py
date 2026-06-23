import numpy as np
import streamlit as st

from strange_attractor_visualiser.attractors.registry import ATTRACTORS
from strange_attractor_visualiser.ui.figure import build_figure, build_static_data
from strange_attractor_visualiser.ui.plot_page import downsample_points
from strange_attractor_visualiser.ui.sidebar import _apply_preset, _reset_parameters


def test_reset_parameters_increments_version():
    st.session_state.clear()
    config = ATTRACTORS["Lorenz"]
    selected_name = "Lorenz"

    _reset_parameters(config, selected_name)
    v1 = st.session_state.get(f"{selected_name}_version", 0)

    _reset_parameters(config, selected_name)
    v2 = st.session_state.get(f"{selected_name}_version", 0)

    assert v2 == v1 + 1


def test_apply_preset_updates_session_state_and_unknown_is_noop():
    st.session_state.clear()
    config = ATTRACTORS["Rossler"]
    selected_name = "Rossler"

    _apply_preset(config, selected_name, "Classic")
    version = st.session_state.get(f"{selected_name}_version", 0)
    assert version > 0

    for k, v in config.presets["Classic"].items():
        assert st.session_state[f"{selected_name}_{k}_v{version}"] == v

    _apply_preset(config, selected_name, "__does_not_exist__")
    v2 = st.session_state.get(f"{selected_name}_version", 0)
    assert v2 > version

    for k, v in config.presets["Classic"].items():
        assert st.session_state[f"{selected_name}_{k}_v{version}"] == v
        assert st.session_state.get(f"{selected_name}_{k}_v{v2}") is None


def test_downsample_points_respects_display_cap():
    x = list(range(10_000))
    y = list(range(10_000))
    z = list(range(10_000))

    x_plot, y_plot, z_plot = downsample_points(x, y, z, max_points=8_000)

    assert len(x_plot) == 8_000
    assert len(y_plot) == len(x_plot)
    assert len(z_plot) == len(x_plot)


def test_build_static_data_supports_lines_with_points():
    values = np.arange(5)
    marker = {"size": 1.25, "color": np.linspace(0, 1, 5), "colorscale": "Viridis"}

    trace, _ = build_static_data(
        values, values + 1, values + 2, marker, display_mode="Lines + points"
    )

    assert trace["mode"] == "lines+markers"
    assert trace["marker"]["color"] == marker["color"].tolist()
    assert "line" in trace


def test_build_static_data_supports_lines_only():
    values = np.arange(5)

    trace, _ = build_static_data(
        values, values + 1, values + 2, {"size": 1.25}, display_mode="Lines"
    )

    assert trace["mode"] == "lines"
    assert "line" in trace
    assert "marker" not in trace


def test_build_figure_animation_supports_lines_only():
    values = np.arange(20)

    fig = build_figure(
        values,
        values + 1,
        values + 2,
        {"size": 1.25},
        animate=True,
        display_mode="Lines",
    )

    assert fig.data[0].mode == "lines"
    assert fig.frames[0].data[0].mode == "lines"
