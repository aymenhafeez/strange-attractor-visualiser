import numpy as np
import plotly.graph_objects as go


def _as_mapping(plotly_obj: go.layout.Updatemenu | go.layout.Slider) -> dict:
    if hasattr(plotly_obj, "to_plotly_json"):
        return plotly_obj.to_plotly_json()
    return dict(plotly_obj)


def build_figure(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, marker_dict: dict, animate: bool
) -> go.Figure:
    marker_style = dict(marker_dict)
    marker_style.setdefault("opacity", 0.74)
    use_density_coloring = "color" in marker_style
    if not use_density_coloring:
        marker_style.setdefault("color", "#d5d5d5")

    if animate:
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
                    "x": 0.1,
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
        if use_density_coloring:
            fig.add_trace(
                go.Scatter3d(x=x, y=y, z=z, mode="markers", marker=marker_style)
            )
        else:
            _add_faded_point_traces(fig, x, y, z, marker_style)

    styled_updatemenus = []
    for menu in fig.layout.updatemenus:
        menu_dict = _as_mapping(menu)
        styled_updatemenus.append({
            **menu_dict,
            "bgcolor": "rgba(26, 26, 26, 0.92)",
            "bordercolor": "#a8a8a8",
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
            "bgcolor": "rgba(16, 16, 16, 0.95)",
            "bordercolor": "#8f8f8f",
            "borderwidth": 1,
            "tickcolor": "#c4c4c4",
            "font": {"family": "Share Tech Mono, monospace", "size": 12},
            "currentvalue": current_value,
        })

    fig.update_layout(
        autosize=True,
        showlegend=False,
        margin=dict(l=10, r=10, b=10, t=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Share Tech Mono, monospace", color="#d8d8d8", size=14),
        scene=dict(
            xaxis=dict(
                title=dict(text="x", font=dict(color="rgba(198, 198, 198, 0.8)")),
                showgrid=True,
                gridcolor="rgba(168, 168, 168, 0.15)",
                zeroline=True,
                backgroundcolor="rgba(21, 21, 21, 0.35)",
                color="#DA5700",
                tickfont=dict(color="rgba(198, 198, 198, 0.8)"),
                showspikes=True,
                spikecolor="#CD8929",
                spikethickness=3,
            ),
            yaxis=dict(
                title=dict(text="y", font=dict(color="rgba(198, 198, 198, 0.8)")),
                showgrid=True,
                gridcolor="rgba(168, 168, 168, 0.15)",
                zeroline=True,
                backgroundcolor="rgba(19, 19, 19, 0.35)",
                color="#DA5700",
                tickfont=dict(color="rgba(198, 198, 198, 0.8)"),
                showspikes=True,
                spikecolor="#CD8929",
                spikethickness=3,
            ),
            zaxis=dict(
                title=dict(text="z", font=dict(color="rgba(198, 198, 198, 0.8)")),
                showgrid=True,
                gridcolor="rgba(168, 168, 168, 0.15)",
                zeroline=True,
                backgroundcolor="rgba(15, 15, 15, 0.3)",
                color="#DA5700",
                tickfont=dict(color="rgba(198, 198, 198, 0.8)"),
                showspikes=True,
                spikecolor="#CD8929",
                spikethickness=3,
            ),
            camera=dict(
                eye=dict(x=1.65, y=1.18, z=0.9),
            ),
        ),
        updatemenus=styled_updatemenus,
        sliders=styled_sliders,
    )

    return fig
