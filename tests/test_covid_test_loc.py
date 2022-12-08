import os,sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from covid_info.data_process import DataProcessor
from covid_info import __version__

def test_version():
    assert __version__ == '0.1.0'

def test_data_dir():
    
    p = DataProcessor("data")
    res_sheet = p.get_all_sheets_from_xls()
    assert all([
        type(res_sheet) == list,
        len(res_sheet) == 3
    ])
