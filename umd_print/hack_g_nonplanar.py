import re
import argparse

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('max_height', metavar='max_height', type=int)
    # parser.add_argument('')

    folder= r"../test_models/test_gcode/{}"
    in_file = folder.format('test_nonplanar.g')
    out_file = folder.format('test_nonplanar-filtered.g')
    max_height = 5

    with open(in_file, 'r') as f:
        regex = r"Z(\d+\.\d+)"
        pat = re.compile(regex)
        new_lines=[]
        for line in f:
            m = re.search(pat, line)
            if m and float(m.group(1)) > max_height:
                # print(line)   
                pass
            else:    
                new_lines.append(line)
        # print(new_lines)
        file = open(out_file, 'w')
        file.writelines(new_lines)
        file.close()
        

        