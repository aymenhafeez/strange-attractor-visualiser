import streamlit as st

from attractors import ATTRACTORS, get_default_params
from plot import _apply_preset, _reset_parameters


def test_reset_parameters_sets_expected_session_state_keys():
    st.session_state.clear()
    config = ATTRACTORS["Lorenz"]
    selected_name = "Lorenz"
    _reset_parameters(config, selected_name)

    defaults = get_default_params(config)

    for param_name, default_val in defaults.items():
        key = f"{selected_name}_{param_name}"
        assert st.session_state[key] == default_val


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
