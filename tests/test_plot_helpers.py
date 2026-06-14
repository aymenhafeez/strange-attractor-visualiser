import streamlit as st

from strange_attractor_visualiser.attractors.registry import ATTRACTORS
from strange_attractor_visualiser.ui.sidebar import _apply_preset, _reset_parameters


def test_reset_parameters_increments_version():
    st.session_state.clear()
    config = ATTRACTORS["Lorenz"]
    selected_name = "Lorenz"

    _reset_parameters(config, selected_name)
    v1 = st.session_state.get(f"{selected_name}_version", 0)

    _reset_parameters(config, selected_name)
    v2 = st.session_state.get(f"{selected_name}_version", 0)

    assert v2 == v1 + 1


def test_apply_preset_updates_session_state_and_unknown_is_noop():
    st.session_state.clear()
    config = ATTRACTORS["Rossler"]
    selected_name = "Rossler"

    _apply_preset(config, selected_name, "Classic")

    for k, v in config.presets["Classic"].items():
        assert st.session_state[f"{selected_name}_{k}"] == v

    before = dict(st.session_state)
    _apply_preset(config, selected_name, "__does_not_exist__")
    assert dict(st.session_state) == before
