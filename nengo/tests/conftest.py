import numpy as np
import pytest

import nengo
import nengo.utils.numpy as npext


def pytest_funcarg__Simulator(request):
    """the Simulator class being tested.

    Please use this, and not nengo.Simulator directly,
    unless the test is reference simulator specific.
    """
    return nengo.Simulator


def pytest_funcarg__RefSimulator(request):
    """the reference simulator.

    Please use this if the test is reference simulator specific.
    Other simulators may choose to implement the same API as the
    reference simulator; this allows them to test easily.
    """
    return nengo.Simulator


def function_seed(function, mod=0):
    c = function.__code__
    return (hash((c.co_filename, c.co_name)) + mod) % npext.maxint


def pytest_funcarg__rng(request):
    # add 1 to seed to be different from network seed
    seed = function_seed(request.function, mod=1)
    return np.random.RandomState(seed)


def pytest_funcarg__seed(request):
    return function_seed(request.function)


def pytest_generate_tests(metafunc):
    if "nl" in metafunc.funcargnames:
        metafunc.parametrize("nl", [nengo.LIF, nengo.LIFRate, nengo.Direct])
    if "nl_nodirect" in metafunc.funcargnames:
        metafunc.parametrize("nl_nodirect", [nengo.LIF, nengo.LIFRate])


def pytest_addoption(parser):
    parser.addoption('--benchmarks', action='store_true', default=False,
                     help='Also run benchmarking tests')
    parser.addoption('--noexamples', action='store_false', default=True,
                     help='Do not run examples')
    parser.addoption(
        '--optional', action='store_true', default=False,
        help='Also run optional tests that may use optional packages')


def pytest_runtest_setup(item):
    for mark, option, message in [
            ('benchmark', 'benchmarks', "benchmarks not requested"),
            ('example', 'noexamples', "examples not requested"),
            ('optional', 'optional', "optional tests not requested")]:
        if getattr(item.obj, mark, None) and not item.config.getvalue(option):
            pytest.skip(message)
