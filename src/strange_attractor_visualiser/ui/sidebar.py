import random
from typing import Any

import numpy as np
import streamlit as st
from scipy.stats import gaussian_kde
from streamlit.delta_generator import DeltaGenerator

from ..attractors.registry import (
    ATTRACTORS,
)
from ..core.models import AttractorConfig
from ..core.solver import get_default_params


def _reset_parameters(config: AttractorConfig, selected_name: str):
    params = get_default_params(config)
    for param_name, default_val in params.items():
        key = f"{selected_name}_{param_name}"
        st.session_state[key] = default_val


def _apply_preset(config: AttractorConfig, selected_name: str, preset_name: str):
    preset = config.presets.get(preset_name, {})
    for param_name, value in preset.items():
        key = f"{selected_name}_{param_name}"
        st.session_state[key] = value


def _random_param_values(config: AttractorConfig, selected_name: str):
    for param in config.params:
        key = f"{selected_name}_{param.name}"
        st.session_state[key] = random.uniform(param.min_val, param.max_val)


def select_attractor_ui(
    config_container: DeltaGenerator,
) -> tuple[bool, AttractorConfig, str]:
    learn_mode = config_container.toggle("Learn mode", value=False)
    selected_name = config_container.selectbox(
        "Select attractor", options=list(ATTRACTORS.keys())
    )
    config = ATTRACTORS[selected_name]

    return learn_mode, config, selected_name


def render_parameter_controls(
    config: AttractorConfig, config_container: DeltaGenerator, selected_name: str
) -> dict[str, float]:
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

    return param_values


def render_learn_panel(
    learn_mode: bool,
    config_container: DeltaGenerator,
    config: AttractorConfig,
    selected_name: str,
):
    if learn_mode:
        config_container.subheader("Overview")
        config_container.write(config.description)
        config_container.markdown(
            f"**Equations**  {config.equation_text}",
            help="These define how x, y, z change over time.",
        )
        if config.prompts:
            config_container.subheader("Try this")
            for prompt in config.prompts:
                config_container.write(f"- {prompt}")

        preset_names = list(config.presets.keys())
        if preset_names:
            selected_preset = config_container.selectbox("Preset", options=preset_names)
            config_container.button(
                "Apply preset",
                on_click=_apply_preset,
                args=(config, selected_name, selected_preset),
            )


def filter_saved_values(show_all: bool, selected_name: str) -> list[dict[str, Any]]:
    filtered = (
        st.session_state.saved_values
        if show_all
        else [
            entry
            for entry in st.session_state.saved_values
            if entry.get("attractor") == selected_name
        ]
    )

    return filtered


def build_saved_rows(filtered: list[Any]) -> list[dict[str, Any]]:
    rows = []
    for idx, entry in enumerate(filtered, start=1):
        row = {"set": idx, "attractor": entry.get("attractor")}
        row.update(entry.get("params", {}))
        rows.append(row)

    return rows


def render_saved_values_ui(
    selected_name: str,
    config_container: DeltaGenerator,
    config: AttractorConfig,
    param_values: dict,
):
    reset_button, save_button, randomise_button = config_container.columns(3)
    reset_button.button(
        "Reset",
        help="Reset parameter values",
        on_click=_reset_parameters,
        args=(config, selected_name),
    )

    if save_button.button("Save values", help="Save parameter values"):
        st.session_state.saved_values.append({
            "attractor": selected_name,
            "params": {param.name: param_values[param.name] for param in config.params},
        })

    if st.session_state.saved_values:
        config_container.subheader("Saved parameter sets")
        show_all = config_container.checkbox("Show all attractors", value=False)
        filtered = filter_saved_values(show_all, selected_name)
        rows = build_saved_rows(filtered)
        config_container.caption(
            f"Showing: {len(filtered)} of {len(st.session_state.saved_values)}"
        )
        with config_container.expander("Show saved values", expanded=False):
            st.dataframe(
                rows,
                hide_index=True,
            )

    randomise_button.button(
        "Randomise",
        help="Randomise parameter values",
        on_click=_random_param_values,
        args=(config, selected_name),
    )


def compute_marker_style(
    config: AttractorConfig,
    x: np.ndarray,
    y: np.ndarray,
    use_density: bool,
    colourscale: str | None,
) -> dict[str, Any]:
    n = config.time_defaults["n"]
    if use_density:
        sample_size = min(1000, n)
        indices = np.random.choice(n, sample_size, replace=False)
        kde = gaussian_kde(np.vstack([x[indices], y[indices]]))
        density = kde(np.vstack([x, y]))
        marker_dict = dict(size=1, color=density, colorscale=colourscale)
    else:
        marker_dict = dict(size=1)

    return marker_dict
