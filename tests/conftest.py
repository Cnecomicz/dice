from pytest import fixture


class MockRng:
    def __init__(self, *values):
        self.values = iter(values)

    def randint(self, low, high):
        return next(self.values)


@fixture
def mock_rng():
    return MockRng
