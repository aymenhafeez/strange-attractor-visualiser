import plotly.express as px
import streamlit as st
import numpy as np

from ..attractors.registry import ATTRACTORS
from ..components.plotly_fast import plotly_fast
from ..core.solver import solve_attractor
from ..ui.figure import build_figure, build_static_data
from ..ui.plane_figures import x_y_plane, x_z_plane, y_z_plane
from ..ui.sidebar import (
    compute_marker_style,
    render_horizontal_parameter_controls,
    render_info_panel,
    render_parameter_controls,
    render_saved_values_ui,
    select_attractor_ui,
)
from ..ui.theme import apply_theme


def init_page():
    st.set_page_config(layout="wide")
    apply_theme()


def downsample_points(x, y, z, max_points: int):
    if len(x) <= max_points:
        return x, y, z

    indices = np.linspace(0, len(x) - 1, max_points, dtype=int)

    if isinstance(x, list):
        return (
            [x[i] for i in indices],
            [y[i] for i in indices],
            [z[i] for i in indices],
        )

    return x[indices], y[indices], z[indices]


def render_plot_page():
    init_page()

    simple_mode = st.toggle("SIMPLE UI", key="simple-mode-toggle")

    if simple_mode:
        st.markdown(
            "<style>[data-testid='stSidebar'] { display: none !important; } </style>",
            unsafe_allow_html=True,
        )
        simple_panel = st.container(key="simple-panel")
        selected_name = simple_panel.radio(
            "ATTRACTOR",
            options=list(ATTRACTORS.keys()),
            label_visibility="collapsed",
        )
        config = ATTRACTORS[selected_name]
        param_values = render_horizontal_parameter_controls(
            config, simple_panel, selected_name
        )
        use_density = False
        colourscale = None
        animate = False
    else:
        controls_section = st.sidebar.container(key="sb-section-controls")
        config, selected_name = select_attractor_ui(controls_section)
        show_info = controls_section.toggle(
            "SHOW ATTRACTOR INFO", value=False, key="toggle_attractor_info"
        )
        if config.description and show_info:
            render_info_panel(True, controls_section, config)

        if "saved_values" not in st.session_state:
            st.session_state.saved_values = []

        parameter_section = st.sidebar.container(key="sb-section-parameters")
        parameter_section.markdown("### Parameters")
        param_values = render_parameter_controls(
            config, parameter_section, selected_name
        )

        saved_section = st.sidebar.container(key="sb-section-saved")
        render_saved_values_ui(selected_name, saved_section, config, param_values)

    if simple_mode:
        st.container(key="simple-equation").markdown(config.equation_text)

    solution = solve_attractor(config, param_values)
    x, y, z = solution.T

    MAX_DISPLAY_POINTS = 8000
    x, y, z = downsample_points(x, y, z, MAX_DISPLAY_POINTS)

    plot_shell = st.container(key="plot-shell")

    if not simple_mode:
        right_rail = plot_shell.container(key="rp-rail")

        display_section = right_rail.container(key="rp-section-display")
        display_section.markdown("### Display")
        use_density = display_section.toggle(
            "USE DENSITY COLOURING (SLOWER PERFORMANCE)", value=False
        )

        colourscale_list = px.colors.named_colorscales()
        colourscale = display_section.selectbox(
            "DENSITY COLOURSCALE",
            options=colourscale_list,
            label_visibility="collapsed",
        )

        run_section = right_rail.container(key="rp-section-run")
        run_section.markdown("### Run")
        animate = run_section.toggle("ANIMATE TRAJECTORY", value=False)

        status_section = right_rail.container(key="rp-section-status")
        status_section.markdown(f"### System: {config.name}")
        status_section.markdown(config.equation_text)

        plane_plot = right_rail.container(key="rp-section-plot")
        plane_plot.markdown("### Projections")
        for img in (x_y_plane(x, y), x_z_plane(x, z), y_z_plane(y, z)):
            plane_plot.image(img, use_container_width=False, width=180)

    marker_dict = compute_marker_style(x, y, use_density, colourscale)

    plot_frame = plot_shell.container(key="plot-frame")

    if animate:
        fig = build_figure(x, y, z, marker_dict, animate)
        plot_frame.plotly_chart(
            fig,
            width="stretch",
            height="stretch",
            config={"responsive": True},
            key="main-attractor-plot",
        )
    else:
        trace, layout = build_static_data(x, y, z, marker_dict)
        with plot_frame:
            plotly_fast(trace, layout, key="main-attractor-plot")

    html = '<div class="status-bar">'
    html += '<span class="status-info">'
    html += "<span><strong>SYSTEM:</strong> " + str(selected_name) + "</span>"
    html += (
        f"<span><strong>INITIAL CONDITIONS:</strong> {config.initial_conditions}"
        + "</span>"
    )
    if param_values:
        params_parts = []
        for k, v in param_values.items():
            name = k.strip("$")
            params_parts.append("<strong>" + name + ":</strong> " + f"{v:.2f}")
        html += "<span>" + "  ".join(params_parts) + "</span>"
    html += "</span></div>"
    plot_shell.markdown(html, unsafe_allow_html=True)
