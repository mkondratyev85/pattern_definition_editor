import pickle

import ezdxf

# load pattern definition from file
filename = '/tmp/pd.pickle'
with open(filename, 'rb') as f:
    pattern_definition = pickle.load(f)

doc = ezdxf.new('R2010')
msp = doc.modelspace()
hatch = msp.add_hatch()  # by default a SOLID fill
hatch.set_pattern_fill('MY_PATTERN',
                       definition=pattern_definition,
                       scale=0.01
                       )
hatch.paths.add_polyline_path(
    [(0, 0), (0, 3), (3, 6), (6, 6), (6, 3), (3, 0)],
    )
doc.saveas(f"/tmp/example.dxf")  # save DXF drawing
