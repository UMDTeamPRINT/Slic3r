import re

fname = "../test_models/test_gcode/test_nonplanar.g"

with open(fname, 'r') as f:

    for line in f:
        print(line, end='')
