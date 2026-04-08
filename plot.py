from typing import Any

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import gaussian_kde
from streamlit.delta_generator import DeltaGenerator

from attractors import (
    ATTRACTORS,
    AttractorConfig,
    get_default_params,
    solve_attractor,
)


def _reset_parameters(config: AttractorConfig, selected_name: str):
    params = get_default_params(config)
    for param_name, default_val in params.items():
        key = f"{selected_name}_{param_name}"
        st.session_state[key] = default_val


def _apply_preset(config: AttractorConfig, selected_name: str, preset_name: str):
    preset = config.presets.get(preset_name, {})
    for param_name, value in preset.items():
        key = f"{selected_name}_{param_name}"
        st.session_state[key] = value


def init_page():
    st.set_page_config(layout="centered")
    st.title("Strange Attractor Visualiser")


def select_attractor_ui(
    config_container: DeltaGenerator,
) -> tuple[bool, AttractorConfig, str]:
    learn_mode = config_container.toggle("Learn mode", value=False)
    selected_name = config_container.selectbox(
        "Select attractor", options=list(ATTRACTORS.keys())
    )
    config = ATTRACTORS[selected_name]

    return learn_mode, config, selected_name


def render_parameter_controls(
    config: AttractorConfig, config_container: DeltaGenerator, selected_name: str
) -> dict[str, float]:
    param_values = {}
    for param in config.params:
        value = config_container.slider(
            param.name,
            min_value=param.min_val,
            max_value=param.max_val,
            value=param.default,
            step=param.step,
            key=f"{selected_name}_{param.name}",
        )
        param_values[param.name] = value

    return param_values


def render_learn_panel(
    learn_mode: bool,
    config_container: DeltaGenerator,
    config: AttractorConfig,
    selected_name: str,
):
    if learn_mode:
        config_container.subheader("Overview")
        config_container.write(config.description)
        config_container.markdown(
            f"**Equations**  {config.equation_text}",
            help="These define how x, y, z change over time.",
        )
        if config.prompts:
            config_container.subheader("Try this")
            for prompt in config.prompts:
                config_container.write(f"- {prompt}")

        preset_names = list(config.presets.keys())
        if preset_names:
            selected_preset = config_container.selectbox("Preset", options=preset_names)
            config_container.button(
                "Apply preset",
                on_click=_apply_preset,
                args=(config, selected_name, selected_preset),
            )


def filter_saved_values(show_all: bool, selected_name: str) -> list[dict[str, Any]]:
    filtered = (
        st.session_state.saved_values
        if show_all
        else [
            entry
            for entry in st.session_state.saved_values
            if entry.get("attractor") == selected_name
        ]
    )

    return filtered


def build_saved_rows(filtered: list[Any]) -> list:
    rows = []
    for idx, entry in enumerate(filtered, start=1):
        row = {"set": idx, "attractor": entry.get("attractor")}
        row.update(entry.get("params", {}))
        rows.append(row)

    return rows


def render_saved_values_ui(
    selected_name: str,
    config_container: DeltaGenerator,
    config: AttractorConfig,
    param_values: dict,
):
    reset_button, save_button = config_container.columns(2)
    reset_button.button(
        "Reset", on_click=_reset_parameters, args=(config, selected_name)
    )

    if save_button.button("Save values"):
        st.session_state.saved_values.append({
            "attractor": selected_name,
            "params": {param.name: param_values[param.name] for param in config.params},
        })

    if st.session_state.saved_values:
        config_container.subheader("Saved parameter sets")
        show_all = config_container.checkbox("Show all attractors", value=False)
        filtered = filter_saved_values(show_all, selected_name)
        rows = build_saved_rows(filtered)
        config_container.caption(
            f"Showing: {len(filtered)} of {len(st.session_state.saved_values)}"
        )
        with config_container.expander("Show saved values", expanded=False):
            config_container.dataframe(
                rows,
                use_container_width=True,
                hide_index=True,
            )


def compute_marker_style(
    config: AttractorConfig,
    x: np.ndarray,
    y: np.ndarray,
    use_density: bool,
    colourscale: str | None,
) -> dict[str, Any]:
    n = config.time_defaults["n"]
    if use_density:
        sample_size = min(1000, n)
        indices = np.random.choice(n, sample_size, replace=False)
        kde = gaussian_kde(np.vstack([x[indices], y[indices]]))
        density = kde(np.vstack([x, y]))
        marker_dict = dict(size=1, color=density, colorscale=colourscale)
    else:
        marker_dict = dict(size=1)

    return marker_dict


def build_figure(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, marker_dict: dict, animate: bool
) -> go.Figure:
    if animate:
        step = max(1, len(x) // 300)

        frames = [
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=x[:i], y=y[:i], z=z[:i], mode="markers", marker=marker_dict
                    )
                ],
                name=str(i),
            )
            for i in range(step, len(x), step)
        ]

        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=x[:step],
                    y=y[:step],
                    z=z[:step],
                    mode="markers",
                    marker=marker_dict,
                )
            ],
            frames=frames,
        )

        fig.update_layout(
            updatemenus=[
                {
                    "type": "buttons",
                    "showactive": False,
                    "x": 0.1,
                    "y": 0,
                    "buttons": [
                        {
                            "label": "▶ Play",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 50, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                        {
                            "label": "⏸ Pause",
                            "method": "animate",
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                    ],
                }
            ],
            sliders=[
                {
                    "active": 0,
                    "yanchor": "top",
                    "y": 0,
                    "xanchor": "left",
                    "x": 0.25,
                    "currentvalue": {
                        "prefix": "Frame: ",
                        "visible": True,
                        "xanchor": "right",
                    },
                    "pad": {"b": 10, "t": 50},
                    "len": 0.7,
                    "steps": [
                        {
                            "args": [
                                [f.name],
                                {
                                    "frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 0},
                                },
                            ],
                            "label": str(i),
                            "method": "animate",
                        }
                        for i, f in enumerate(frames)
                    ],
                }
            ],
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="markers", marker=marker_dict))

    fig.update_layout(
        width=700,
        height=700,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(
                eye=dict(x=0, y=1, z=1),
            ),
        ),
    )

    return fig


def render_plot_page():
    init_page()

    plot_container = st.container()
    config_container = st.sidebar.container()
    learn_mode, config, selected_name = select_attractor_ui(config_container)

    if "saved_values" not in st.session_state:
        st.session_state.saved_values = []

    render_learn_panel(learn_mode, config_container, config, selected_name)

    param_values = render_parameter_controls(config, config_container, selected_name)

    render_saved_values_ui(selected_name, config_container, config, param_values)

    solution = solve_attractor(config, param_values)
    x, y, z = solution.T

    use_density = config_container.checkbox(
        "Use density colouring (slower performance)", value=False
    )

    colourscale_list = px.colors.named_colorscales()
    colourscale = config_container.selectbox(
        "Density colorscale", options=colourscale_list
    )

    marker_dict = compute_marker_style(config, x, y, use_density, colourscale)

    animate = config_container.checkbox("Animate trajectory", value=False)

    fig = build_figure(x, y, z, marker_dict, animate)
    plot_container.plotly_chart(fig, width="stretch")
