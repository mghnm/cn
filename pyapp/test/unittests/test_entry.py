from datetime import datetime
import pytest
from entry import Entry


@pytest.fixture
def new_entry():
    return Entry("John", "Doe", "Hello, World!")


def test_entry_properties(new_entry):
    assert new_entry.firstname == "John"
    assert new_entry.lastname == "Doe"
    assert new_entry.message == "Hello, World!"


def test_entry_entrytime_default(new_entry):
    # Ensure entrytime is set to the current UTC time when not provided
    assert isinstance(new_entry.entrytime, datetime)
    assert new_entry.entrytime <= datetime.utcnow()


def test_entry_entrytime_custom():
    custom_entrytime = datetime(2022, 1, 1, 12, 0, 0)
    entry = Entry("Jane", "Smith", "Test", entrytime=custom_entrytime)
    assert entry.entrytime == custom_entrytime