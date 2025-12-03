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


To generate code coverage reports:

Compile with. 

`FFLAGS  = -O0 -fprofile-arcs -ftest-coverage -ffree-line-length-none $(INCS)`

Run

`test_interp.py`


Once the tests have run, run the following in the build directory:

```
lcov --gcov-tool=/opt/local/bin/gcov-mp-14 --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html
```

