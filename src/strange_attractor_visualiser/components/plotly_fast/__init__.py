import os

import streamlit.components.v1 as components


def plotly_fast(trace, layout, key=None):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend")
    component_func = components.declare_component("plotly_fast", path=build_dir)
    component_value = component_func(
        trace=trace,
        layout=layout,
        key=key,
        default=0,
    )
    return component_value
