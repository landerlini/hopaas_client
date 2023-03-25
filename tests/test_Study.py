from hopaas_client import samplers, pruners
import random
import pytest

RANDOM_CODE = random.randint(0, 10000)
suggestions = []


def suggestion(f):
    global suggestions
    suggestions.append(f.__name__)
    return pytest.fixture(f)


@pytest.fixture
def study():
    from hopaas_client import Study
    study = Study('TEST::Study::study', dict(some_value=RANDOM_CODE))
    return study


@suggestion
def suggest_int():
    from hopaas_client.suggestions import Int
    return Int(0, 100)


@suggestion
def suggest_int_with_step():
    from hopaas_client.suggestions import Int
    return Int(0, 100, step=5)


@suggestion
def suggest_int_with_log():
    from hopaas_client.suggestions import Int
    return Int(0, 1000, log=True)


@suggestion
def suggest_float():
    from hopaas_client.suggestions import Float
    return Float(-1., 1.)


@suggestion
def suggest_float_with_step():
    from hopaas_client.suggestions import Float
    return Float(-1., 1., step=0.1)


@suggestion
def suggest_float_with_log():
    from hopaas_client.suggestions import Float
    return Float(1e-3, 1e+3, log=True)


@suggestion
def suggest_categorical():
    from hopaas_client.suggestions import Categorical
    return Categorical(['Charmander', 'Squirtle', 'Bulbasaur'])


###############################################################################


def test_study_instantiation(study):
    from hopaas_client import Study
    assert isinstance(study, Study)


all_samplers = [getattr(samplers, s) for s in samplers.testables]
all_pruners = [getattr(pruners, p) for p in pruners.testables]


@pytest.mark.parametrize('sampler', all_samplers)
@pytest.mark.parametrize('pruner', all_pruners)
@pytest.mark.parametrize('suggested', suggestions)
def test_one_shot(sampler, pruner, suggested, request):
    suggested = request.getfixturevalue(suggested)
    from hopaas_client import Study
    study = Study(
            'Test::Study::one_shot',
            properties={'x': 1, 'y': suggested},
            sampler=sampler(),
            pruner=pruner() if pruner != pruners.ThresholdPruner else pruner(upper=2)
    )

    with study.trial() as trial:
        trial.loss = 1.23


def test_simple_loop(study):
    for iTrial in range(3):
        with study.trial() as trial:
            for i in range(5):
                trial.loss = 1.23


def perform(_):
    from hopaas_client import Study
    study = Study('TEST::Study::multiprocessing', dict(some_value=2))
    with study.trial() as trial:
        for i in range(5):
            trial.loss = 1.23
        return trial.loss


def test_multiprocessing():
    from multiprocessing import Pool
    pool = Pool(5)
    losses = pool.imap_unordered(perform, range(15))
    assert all([ls == 1.23 for ls in losses])


def test_failing_loop(study):
    for iTrial in range(5):
        with study.trial() as trial:
            if iTrial == 2:
                break  # Simulate a failure
            else:
                for i in range(5):
                    trial.loss = 1.23


def compute_xsquared(_):
    from hopaas_client import Study
    from hopaas_client.samplers import TPESampler
    from hopaas_client.suggestions import Uniform

    study = Study("TEST::Study::x_squared",
                  sampler=TPESampler(n_startup_trials=10),
                  properties=dict(
                      x=Uniform(-50, 50),
                      y=None
                  ))

    with study.trial() as trial:
        for iStep in range(1, 11):
            trial.loss = trial.x**2 + random.uniform(0, 10000/iStep)
            if trial.should_prune:
                break


def test_xsquared():
    from multiprocessing import Pool

    with Pool(10) as pool:
        pool.map(compute_xsquared, range(25))
