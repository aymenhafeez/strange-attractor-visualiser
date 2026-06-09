import plotly.express as px
import streamlit as st

from ..core.solver import solve_attractor
from ..ui.figure import build_figure
from ..ui.sidebar import (
    compute_marker_style,
    render_info_panel,
    render_parameter_controls,
    render_saved_values_ui,
    select_attractor_ui,
)
from ..ui.theme import apply_theme, render_hud_header


def init_page():
    st.set_page_config(layout="wide")
    apply_theme()


def render_plot_page():
    init_page()

    config_container = st.sidebar.container()
    render_hud_header(config_container)
    config_container.markdown(
        "<div style='height:1.2rem;'></div>", unsafe_allow_html=True
    )

    system_section = config_container.container(key="sb-section-system")
    attractor_info, config, selected_name = select_attractor_ui(system_section)

    if "saved_values" not in st.session_state:
        st.session_state.saved_values = []

    if attractor_info:
        overview_section = config_container.container(key="sb-section-overview")
        render_info_panel(attractor_info, overview_section, config, selected_name)

    parameter_section = config_container.container(key="sb-section-parameters")
    parameter_section.markdown("### Parameters")
    param_values = render_parameter_controls(config, parameter_section, selected_name)

    render_saved_values_ui(selected_name, parameter_section, config, param_values)

    solution = solve_attractor(config, param_values)
    x, y, z = solution.T

    plot_col, right_rail_col = st.columns([0.78, 0.22], gap=None)
    right_rail = right_rail_col.container(key="rp-rail")

    display_section = right_rail.container(key="rp-section-display")
    display_section.markdown("### Display")
    use_density = display_section.toggle(
        "Use density colouring (slower performance)", value=False
    )

    colourscale_list = px.colors.named_colorscales()
    colourscale = display_section.selectbox(
        "Density colourscale", options=colourscale_list
    )

    run_section = right_rail.container(key="rp-section-run")
    run_section.markdown("### Run")
    animate = run_section.toggle("Animate trajectory", value=False)

    status_section = right_rail.container(key="rp-section-status")
    status_section.markdown("### Status")
    status_section.caption(f"Attractor: {selected_name}")
    status_section.caption(f"Points: {len(x):,}")

    marker_dict = compute_marker_style(config, x, y, use_density, colourscale)

    fig = build_figure(x, y, z, marker_dict, animate)
    plot_col.plotly_chart(
        fig,
        width="stretch",
        config={"responsive": True},
        key="main-attractor-plot",
    )
