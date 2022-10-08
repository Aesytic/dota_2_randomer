import pytest


@pytest.fixture
def mock_session_fixture():
    class MockSession:
        def __init__(self):
            self.add_buffer = []

        def add(self, row):
            self.add_buffer.append(row)

        def commit(self):
            pass

    yield MockSession()
