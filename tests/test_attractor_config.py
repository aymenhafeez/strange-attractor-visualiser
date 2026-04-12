import pytest

from strange_attractor_visualiser.attractors.registry import ATTRACTORS
from strange_attractor_visualiser.core.solver import get_default_params


@pytest.mark.parametrize("name,config", ATTRACTORS.items())
def test_get_default_params_matches_config_defaults(name, config):
    defaults = get_default_params(config)
    expected_names = [p.name for p in config.params]
    assert set(defaults.keys()) == set(expected_names)

    for p in config.params:
        assert defaults[p.name] == p.default


@pytest.mark.parametrize("name,config", ATTRACTORS.items())
def test_defaults_within_bounds(name, config):

    for p in config.params:
        assert p.min_val <= p.default <= p.max_val


@pytest.mark.parametrize("name,config", ATTRACTORS.items())
def test_presets_only_use_declared_param_names(name, config):
    valid = {p.name for p in config.params}

    for _, preset in config.presets.items():
        assert set(preset.keys()).issubset(valid)
