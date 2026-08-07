from typing import Callable

from pytest import fixture

class MockRng:
    def __init__(self, value):
        self.value = value

    def randint(self, low, high):
        return self.value


@fixture
def mock_rng():
    return lambda value: MockRng(value)