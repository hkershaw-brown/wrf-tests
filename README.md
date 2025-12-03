## Tests to compare results from one version of wrf model_mod_check to another


test_interp.py 
 - generates random points & qtys with a wrf domain
 - runs model_mod_check for 2 model_mod_checks for the random points * [vertisheight, etc.]

```
test_interp.py -vv -x
```

test_case_to_namelist.py
- generates namelist info to copy and paste to run model_mod_check

```
python test_case_to_namelist.py '((359.974, 43.298, 463.5), "QTY_POTENTIAL_TEMPERATURE")'  
```
