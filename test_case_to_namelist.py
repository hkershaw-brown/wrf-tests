import sys
import ast

def test_case_to_namelist_entry(test_case):
    loc, qty = test_case
    print(f"   loc_of_interest       = {loc[0]}, {loc[1]}, {loc[2]}")
    print(f"   quantity_of_interest  = '{qty}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py '((lon, lat, height), \"QTY_TYPE\")'")
        sys.exit(1)
    arg = sys.argv[1]
    try:
        test_case = ast.literal_eval(arg)
        test_case_to_namelist_entry(test_case)
    except Exception as e:
        print(f"Error parsing argument: {e}")
        sys.exit(1)
