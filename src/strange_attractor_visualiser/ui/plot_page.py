import plotly.express as px
import streamlit as st

from ..core.solver import solve_attractor
from ..ui.figure import build_figure
from ..ui.plane_figures import x_y_plane, x_z_plane, y_z_plane
from ..ui.sidebar import (
    compute_marker_style,
    render_info_panel,
    render_initial_condition_controls,
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

    ic_section = config_container.container(key="sb-section-ic")
    ic_section.markdown("### Initial Conditions")
    initial_conditions = render_initial_condition_controls(
        config, selected_name, ic_section
    )

    render_saved_values_ui(selected_name, parameter_section, config, param_values)

    solution = solve_attractor(config, param_values, initial_conditions)
    x, y, z = solution.T

    MAX_DISPLAY_POINTS = 8000
    stride = max(1, len(x) // MAX_DISPLAY_POINTS)
    x, y, z = x[::stride], y[::stride], z[::stride]

    plot_col, right_rail_col = st.columns([0.75, 0.25], gap=None)
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

    plane_plot = right_rail.container(key="rp-section-plot")
    plane_plot.markdown("### Projections")
    for img in (x_y_plane(x, y), x_z_plane(x, z), y_z_plane(y, z)):
        plane_plot.image(img, use_container_width=False, width=180)

    marker_dict = compute_marker_style(x, y, use_density, colourscale)

    fig = build_figure(x, y, z, marker_dict, animate)
    plot_col.plotly_chart(
        fig,
        width="stretch",
        config={"responsive": True},
        key="main-attractor-plot",
    )
