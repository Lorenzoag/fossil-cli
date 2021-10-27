import pytest
from click.testing import CliRunner

@pytest.fixture
def invoke():
    return CliRunner().invoke
