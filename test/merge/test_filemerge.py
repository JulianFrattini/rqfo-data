import pytest
import os, json

@pytest.mark.system
def test_versions_existing():
    """This test makes sure that all existing version (i.e., the ones contained in ./versions) are contained in the merged json file (i.e., in ./merged/rqfo-data.json)."""

    # ground truth: existing versions
    existing_versions: list[str] = [filename.split('.')[0] for filename in os.listdir('./versions')]

    # versions included in the merged file
    merged_file: dict = None
    with open('./merged/rqfo-data.json', 'r') as file:
        merged_file = json.load(file)
    included_versions: list[str] = list(merged_file['versions'].keys())

    assert existing_versions == included_versions