""" Unit test for import_data module """
from pathlib import Path
import pytest
from src import import_data as imp


def test_get_files():
    """ test the function get_files_from_dir with empty_dir"""
    path = Path(Path(__file__).parent.resolve(),'tests','empty_dir')
    with pytest.raises(ValueError, match=r'No files to process'):
        imp.get_files_from_dir(path)

def test_get_path_file_from_dir():
    """ test the function get_path_file_from_dir with no drug file"""

    path = Path(Path(__file__).parent.resolve(),'tests','no_drug_dir')
    with pytest.raises(ValueError, match='No files with drugs data'):
        imp.get_path_file_from_dir(path)

def test_import_dir_to_dataframe():
    """ test the function import_dir_to_dataframe with a file containing 0 lines"""

    path = Path(Path(__file__).parent.resolve(),'tests','no_row')
    with pytest.raises(ValueError, match='Missing data'):
        imp.import_dir_to_dataframe(path)
        