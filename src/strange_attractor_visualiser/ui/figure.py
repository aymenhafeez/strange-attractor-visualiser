import numpy as np
import plotly.graph_objects as go


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
