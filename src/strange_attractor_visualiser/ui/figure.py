import numpy as np
import plotly.graph_objects as go


def build_figure(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, marker_dict: dict, animate: bool
) -> go.Figure:
    marker_style = dict(marker_dict)
    marker_style.setdefault("opacity", 0.74)
    if "color" not in marker_style:
        marker_style["color"] = "#d5d5d5"

    if animate:
        step = max(1, len(x) // 300)

        frames = [
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=x[:i], y=y[:i], z=z[:i], mode="markers", marker=marker_style
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
                                    "frame": {"duration": 50, "redraw": True},
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
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="markers", marker=marker_style))

    fig.update_layout(
        width=1050,
        height=760,
        margin=dict(l=10, r=10, b=10, t=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Share Tech Mono, monospace", color="#d8d8d8", size=14),
        scene=dict(
            xaxis=dict(
                title=dict(text="x", font=dict(color="rgba(198, 198, 198, 0.8)")),
                showgrid=True,
                gridcolor="rgba(168, 168, 168, 0.2)",
                backgroundcolor="rgba(21, 21, 21, 0.35)",
                color="#DA5700",
                tickfont=dict(color="rgba(198, 198, 198, 0.8)"),
            ),
            yaxis=dict(
                title=dict(text="y", font=dict(color="rgba(198, 198, 198, 0.8)")),
                showgrid=True,
                gridcolor="rgba(168, 168, 168, 0.2)",
                zeroline=False,
                backgroundcolor="rgba(19, 19, 19, 0.35)",
                color="#DA5700",
                tickfont=dict(color="rgba(198, 198, 198, 0.8)"),
            ),
            zaxis=dict(
                title=dict(text="z", font=dict(color="rgba(198, 198, 198, 0.8)")),
                showgrid=True,
                gridcolor="rgba(168, 168, 168, 0.2)",
                zeroline=False,
                backgroundcolor="rgba(15, 15, 15, 0.3)",
                color="#DA5700",
                tickfont=dict(color="rgba(198, 198, 198, 0.8)"),
            ),
            camera=dict(
                eye=dict(x=1.65, y=1.18, z=0.9),
            ),
        ),
        updatemenus=[
            {
                **menu,
                "bgcolor": "rgba(26, 26, 26, 0.92)",
                "bordercolor": "#a8a8a8",
                "borderwidth": 1,
                "font": {"family": "Share Tech Mono, monospace", "size": 12},
            }
            for menu in fig.layout.updatemenus
        ],
        sliders=[
            {
                **slider,
                "bgcolor": "rgba(16, 16, 16, 0.95)",
                "bordercolor": "#8f8f8f",
                "borderwidth": 1,
                "tickcolor": "#c4c4c4",
                "font": {"family": "Share Tech Mono, monospace", "size": 12},
                "currentvalue": {
                    **slider.currentvalue,
                    "font": {"family": "Share Tech Mono, monospace", "size": 12},
                },
            }
            for slider in fig.layout.sliders
        ],
    )

    return fig
