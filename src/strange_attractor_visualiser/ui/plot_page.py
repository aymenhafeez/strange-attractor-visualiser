import plotly.express as px
import streamlit as st

from ..core.solver import solve_attractor
from ..ui.figure import build_figure
from ..ui.sidebar import (
    compute_marker_style,
    render_learn_panel,
    render_parameter_controls,
    render_saved_values_ui,
    select_attractor_ui,
)


def init_page():
    st.set_page_config(layout="centered")
    st.title("Strange Attractor Visualiser")


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
        "Density colourscale", options=colourscale_list
    )

    marker_dict = compute_marker_style(config, x, y, use_density, colourscale)

    animate = config_container.checkbox("Animate trajectory", value=False)

    fig = build_figure(x, y, z, marker_dict, animate)
    plot_container.plotly_chart(fig, width="stretch")
