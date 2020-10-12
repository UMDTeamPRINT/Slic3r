import re
import argparse

folder= r"/home/froppy/Slic3r/test_models/test_gcode/{}"
in_file = folder.format('fill2-fixed.gcode')
out_file = folder.format('fill2-fixed-flipped.gcode')

offset_z = 4 #mm

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('max_height', metavar='max_height', type=int)
    # parser.add_argument('')


    # Layer 0 = start code
    # Layer length(layers)-1 = end code
    layers = []

    with open(in_file, 'r') as f:
        lines = f.readlines()
        current_layer = []
        layer_regex = re.compile(r'layer \((\d+)\)')  # This is what verbose GCode prints out in Slic3r

        # Parse layers
        for line in lines:
            layer_num = re.search(layer_regex,line)
            if layer_num or 'M107' in line:  # M107 is fan off (represents EOF)
                layers.append(current_layer)
                current_layer=[]
            current_layer.append(line)
        layers.append(current_layer) # Make sure last layer is included (EOF)

        new_layers = []
        
        # Begin with start up code
        new_layers.extend(layers[0])

        # Flip print code
        print_layers = layers[1:-1]
        print_layers = [x for x in reversed(print_layers)] # Reverses layer order

        # Mirror Z values

        # Find max height
        regex = r"Z(\d+\.\d+)"
        pat = re.compile(regex)
        max_z = 0
        for layer in print_layers:
            for line in layer:
                m = re.search(pat, line)
                if m and float(m.group(1)) > max_z:
                    max_z = float(m.group(1))
        # Mirror
        new_print_layers = []
        for layer in print_layers:
            new_layer = []
            for line in layer:
                m = re.search(pat, line)
                if m: 
                    if 'Move up' in line or 'Move down' in line:
                        pass # TODO maybe find something better than deleting them lol
                    else:
                        old_z = float(m.group(1))
                        new_z = max_z - old_z + offset_z
                        new_line = pat.sub(r'Z{:.3f}'.format(new_z), line)  # Replace with new Z
                        new_layer.append(new_line)
                else:
                    new_layer.append(line)
            new_print_layers.extend(new_layer)
        new_layers.extend(new_print_layers)

        # End with end code
        new_layers.extend(layers[len(layers)-1])

        # Write to file
        file = open(out_file, 'w')
        file.writelines(new_layers)
        file.close()
        
