import pytest
from mock import patch, mock_open

import json

from src.util.fileloader import read_file

mock_json = {"key": "value"}

@pytest.mark.unit
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(mock_json))
def test_existing_file(mock_file):
    result = read_file(path="test.json")
    assert result == mock_json

@pytest.mark.unit
def test_nonexiting_file():
    with patch('builtins.open', mock_open()) as mock_file:
        mock_file.side_effect = OSError()

        result = read_file(path="test.json")
        assert result == None