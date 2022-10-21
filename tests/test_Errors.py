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
def suggest_float():
    from hopaas_client.suggestions import Float
    return Float(0, 1)


################################################################################

def test_trial_context_error(study):
    try:
        with study.trial() as trial:
            print(1 // 0)
    except ZeroDivisionError:
        return True
    else:
        raise AssertionError("A ZeroDivisionError was masked")



