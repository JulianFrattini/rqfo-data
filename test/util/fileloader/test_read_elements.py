import pytest
from mock import patch, MagicMock

from src.util.fileloader import read_elements


def mock_read_file(path: str):
    if path == 'dir/file1.json':
        return {'name': 'foo'}
    elif path == 'dir/file2.json':
        return {'name': 'bar'}
    return None

@pytest.mark.unit
@patch('os.listdir')
def test_files_existing(mocked_listdir):
    mocked_listdir.return_value = ['file1.json', 'file2.json']

    with patch('src.util.fileloader.read_file') as mocked_read_file:
        mocked_read_file.side_effect = mock_read_file

        result = read_elements(basepath='dir')
        assert result == {'file1': {'name': 'foo'}, 'file2': {'name': 'bar'}}

@pytest.mark.unit
@patch('os.listdir')
def test_files_not_existing(mocked_listdir):
    mocked_listdir.return_value = []

    with patch('src.util.fileloader.read_file') as mocked_read_file:
        mocked_read_file.side_effect = mock_read_file

        result = read_elements(basepath='dir')
        assert result == {}

@pytest.mark.unit
@patch('os.listdir')
def test_whitelist(mocked_listdir):
    mocked_listdir.return_value = ['file1.json', 'file2.json']

    with patch('src.util.fileloader.read_file') as mocked_read_file:
        mocked_read_file.side_effect = mock_read_file

        result = read_elements(basepath='dir', whitelist=['file2.json'])
        assert result == {'file2': {'name': 'bar'}}