import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import gaussian_kde

from attractors import (
    ATTRACTORS,
    get_default_params,
    solve_attractor,
)

st.set_page_config(layout="wide")


def reset_parameters(config, selected_name):
    params = get_default_params(config)
    for param_name, default_val in params.items():
        key = f"{selected_name}_{param_name}"
        st.session_state[key] = default_val


def plot_attractor():
    st.title("Strange Attractor Visualiser")
    st.caption("Interactive 3D exploration of classic chaotic systems.")

    plot_container = st.container()
    config_container = st.sidebar.container(border=True)

    selected_name = config_container.selectbox(
        "Select attractor", options=list(ATTRACTORS.keys())
    )
    config = ATTRACTORS[selected_name]

    if "saved_values" not in st.session_state:
        st.session_state.saved_values = []

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

    reset_button, save_button = config_container.columns(2)
    reset_button.button(
        "Reset", on_click=reset_parameters, args=(config, selected_name)
    )

    if save_button.button("Save values"):
        st.session_state.saved_values.append(
            {param.name: param_values[param.name] for param in config.params}
        )

    if st.session_state.saved_values:
        config_container.subheader("Saved parameter sets")
        for idx, values in enumerate(st.session_state.saved_values, start=1):
            config_container.write(f"#{idx}")
            config_container.json(values)

    solution = solve_attractor(config, param_values)
    x, y, z = solution.T

    use_density = config_container.checkbox(
        "Use density colouring (slower performance)", value=False
    )

    colorscale_list = px.colors.named_colorscales()
    colorscale = config_container.selectbox(
        "Density colorscale", options=colorscale_list
    )

    n = config.time_defaults["n"]
    if use_density:
        sample_size = min(1000, n)
        indices = np.random.choice(n, sample_size, replace=False)
        kde = gaussian_kde(np.vstack([x[indices], y[indices]]))
        density = kde(np.vstack([x, y]))
        marker_dict = dict(size=0.4, color=density, colorscale=colorscale)
    else:
        marker_dict = dict(size=0.4)

    animate = config_container.checkbox("Animate trajectory", value=False)
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
        width=800,
        height=800,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(
                eye=dict(x=0, y=1, z=1),
            ),
        ),
    )

    plot_container.plotly_chart(fig, width="stretch")
