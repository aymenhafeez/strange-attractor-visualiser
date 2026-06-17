import numpy as np
import plotly.graph_objects as go

_PLOT_THEME = {
    "font": "#999999",
    "axis_title": "rgba(120, 120, 120, 0.8)",
    "axis_bg": "rgba(128, 128, 128, 0.06)",
    "axis_color": "#DA5700",
    "grid": "rgba(128, 128, 128, 0.15)",
    "spike": "#CD8929",
    "menu_bg": "rgba(200, 200, 200, 0.12)",
    "menu_border": "#aaaaaa",
    "slider_bg": "rgba(200, 200, 200, 0.08)",
    "slider_border": "#aaaaaa",
    "slider_tick": "#aaaaaa",
    "marker": "#cccccc",
}

_EXT = 3.5


def _as_mapping(plotly_obj: go.layout.Updatemenu | go.layout.Slider) -> dict:
    if hasattr(plotly_obj, "to_plotly_json"):
        return plotly_obj.to_plotly_json()

    return dict(plotly_obj)


def _cr(lo, hi):
    c = (lo + hi) / 2
    h = (hi - lo) / 2 * _EXT

    return c - h, c + h


def _build_animation_figure(x, y, z, marker_style):
    max_anim_points = 12000
    sample_stride = max(1, len(x) // max_anim_points)
    x_anim = x[::sample_stride]
    y_anim = y[::sample_stride]
    z_anim = z[::sample_stride]

    step = max(1, len(x_anim) // 180)

    frames = [
        go.Frame(
            data=[
                go.Scatter3d(
                    x=x_anim[:i],
                    y=y_anim[:i],
                    z=z_anim[:i],
                    mode="markers",
                    marker=marker_style,
                )
            ],
            name=str(i),
        )
        for i in range(step, len(x_anim), step)
    ]

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x_anim[:step],
                y=y_anim[:step],
                z=z_anim[:step],
                mode="markers",
                marker=marker_style,
            )
        ],
        frames=frames,
    )

    fig.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 0.78,
                "y": 0,
                "buttons": [
                    {
                        "label": "PLAY",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 40, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "PAUSE",
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
                "pad": {"b": 4, "t": 8},
                "len": 0.45,
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

    return fig


def _build_grid_annotations(xr, yr, zr, n_ticks):
    anns = []
    for v in np.linspace(xr[0], xr[1], n_ticks):
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=v,
                y=0,
                z=zr[0],
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=v,
                y=0,
                z=zr[1],
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=v,
                y=yr[0],
                z=0,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=v,
                y=yr[1],
                z=0,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
    for v in np.linspace(yr[0], yr[1], n_ticks):
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=0,
                y=v,
                z=zr[0],
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=0,
                y=v,
                z=zr[1],
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=xr[0],
                y=v,
                z=0,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=xr[1],
                y=v,
                z=0,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
    for v in np.linspace(zr[0], zr[1], n_ticks):
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=xr[0],
                y=0,
                z=v,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=xr[1],
                y=0,
                z=v,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=0,
                y=yr[0],
                z=v,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )
        anns.append(
            dict(
                showarrow=False,
                text=f"{v:.1f}",
                x=0,
                y=yr[1],
                z=v,
                font=dict(size=12, color=_PLOT_THEME["axis_title"]),
            )
        )

    return anns


def _style_controls(fig):
    styled_updatemenus = []
    for menu in fig.layout.updatemenus:
        menu_dict = _as_mapping(menu)
        styled_updatemenus.append({
            **menu_dict,
            "bgcolor": _PLOT_THEME["menu_bg"],
            "bordercolor": _PLOT_THEME["menu_border"],
            "borderwidth": 1,
            "font": {"family": "Share Tech Mono, monospace", "size": 12},
        })

    styled_sliders = []
    for slider in fig.layout.sliders:
        slider_dict = _as_mapping(slider)
        current_value = dict(slider_dict.get("currentvalue", {}))
        current_value["font"] = {"family": "Share Tech Mono, monospace", "size": 12}
        styled_sliders.append({
            **slider_dict,
            "bgcolor": _PLOT_THEME["slider_bg"],
            "bordercolor": _PLOT_THEME["slider_border"],
            "borderwidth": 1,
            "tickcolor": _PLOT_THEME["slider_tick"],
            "font": {"family": "Share Tech Mono, monospace", "size": 12},
            "currentvalue": current_value,
        })

    return styled_updatemenus, styled_sliders


def build_figure(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    marker_dict: dict,
    animate: bool,
) -> go.Figure:
    marker_style = dict(marker_dict)
    marker_style.setdefault("opacity", 0.74)
    use_density_coloring = "color" in marker_style
    if not use_density_coloring:
        marker_style.setdefault("color", _PLOT_THEME["marker"])

    if animate:
        fig = _build_animation_figure(x, y, z, marker_style)
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="markers", marker=marker_style))

    x_lo, x_hi = float(np.min(x)), float(np.max(x))
    y_lo, y_hi = float(np.min(y)), float(np.max(y))
    z_lo, z_hi = float(np.min(z)), float(np.max(z))

    xr = _cr(x_lo, x_hi)
    yr = _cr(y_lo, y_hi)
    zr = _cr(z_lo, z_hi)

    n_ticks = 4
    dtick_x = (xr[1] - xr[0]) / (n_ticks - 1)
    dtick_y = (yr[1] - yr[0]) / (n_ticks - 1)
    dtick_z = (zr[1] - zr[0]) / (n_ticks - 1)

    anns = _build_grid_annotations(xr, yr, zr, n_ticks)

    styled_updatemenus, styled_sliders = _style_controls(fig)

    fig.update_layout(
        autosize=True,
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Share Tech Mono, monospace", color=_PLOT_THEME["font"], size=14
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text="x", font=dict(color=_PLOT_THEME["axis_title"])),
                showgrid=True,
                gridcolor=_PLOT_THEME["grid"],
                zeroline=True,
                zerolinecolor=_PLOT_THEME["axis_color"],
                backgroundcolor=_PLOT_THEME["axis_bg"],
                color=_PLOT_THEME["axis_color"],
                tickfont=dict(color=_PLOT_THEME["axis_title"]),
                showticklabels=False,
                showspikes=True,
                spikecolor=_PLOT_THEME["spike"],
                spikethickness=3,
                dtick=dtick_x,
                range=xr,
            ),
            yaxis=dict(
                title=dict(text="y", font=dict(color=_PLOT_THEME["axis_title"])),
                showgrid=True,
                gridcolor=_PLOT_THEME["grid"],
                zeroline=True,
                zerolinecolor=_PLOT_THEME["axis_color"],
                backgroundcolor=_PLOT_THEME["axis_bg"],
                color=_PLOT_THEME["axis_color"],
                tickfont=dict(color=_PLOT_THEME["axis_title"]),
                showticklabels=False,
                showspikes=True,
                spikecolor=_PLOT_THEME["spike"],
                spikethickness=3,
                dtick=dtick_y,
                range=yr,
            ),
            zaxis=dict(
                title=dict(text="z", font=dict(color=_PLOT_THEME["axis_title"])),
                showgrid=True,
                gridcolor=_PLOT_THEME["grid"],
                zeroline=True,
                zerolinecolor=_PLOT_THEME["axis_color"],
                backgroundcolor=_PLOT_THEME["axis_bg"],
                color=_PLOT_THEME["axis_color"],
                tickfont=dict(color=_PLOT_THEME["axis_title"]),
                showticklabels=False,
                showspikes=True,
                spikecolor=_PLOT_THEME["spike"],
                spikethickness=3,
                dtick=dtick_z,
                range=zr,
            ),
            annotations=anns,
            camera=dict(eye=dict(x=1.35 / _EXT, y=0.98 / _EXT, z=0.75 / _EXT)),
        ),
        updatemenus=styled_updatemenus,
        sliders=styled_sliders,
    )

    return fig
