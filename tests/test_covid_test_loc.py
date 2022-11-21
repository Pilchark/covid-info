from covid_test_loc import __version__
import os,sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from covid_test_loc.data_process import DataProcessor

def test_version():
    assert __version__ == '0.1.0'

def test_data_dir():
    
    p = DataProcessor()
    res_sheet = p.get_all_sheets_from_xls()
    assert all([
        type(res_sheet) == list,
        len(res_sheet) == 2
    ])
