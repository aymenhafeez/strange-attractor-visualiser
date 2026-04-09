import numpy as np
import pytest

from strange_attractor_visualiser.attractors.registry import ATTRACTORS
from strange_attractor_visualiser.core.solver import get_default_params, solve_attractor


@pytest.mark.parametrize("name,config", ATTRACTORS.items())
def test_solver_shape_and_finite_all_attractors(name, config):
    params = get_default_params(config)
    sol = solve_attractor(config, params)
    assert sol.shape == (config.time_defaults["n"], 3)
    assert np.isfinite(sol).all()


@pytest.mark.parametrize("name,config", ATTRACTORS.items())
def test_solver_starts_at_initial_conditions(name, config):
    params = get_default_params(config)
    sol = solve_attractor(config, params)
    assert np.allclose(sol[0], config.initial_conditions, atol=1e-6)


def test_solver_missing_param_raises_keyerror():
    config = ATTRACTORS["Lorenz"]
    params = get_default_params(config)
    params.pop("$\\rho$")

    with pytest.raises(KeyError):
        solve_attractor(config, params)
