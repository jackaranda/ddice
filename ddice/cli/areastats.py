import sys
import os.path

import numpy as np

from ddice.dataset import Dataset, netCDF4Dataset
from ddice.variable import Variable, Dimension
from ddice.field import CFField
from ddice.field import grouping

from shapely.geometry import shape
from fiona import collection


# Reading source data
filename, varname = sys.argv[1].split(':')
print('opening', filename, varname)

ds = netCDF4Dataset(filename)
print(ds)

field = CFField(ds.variables[varname])
print('field', field.shape)

if len(sys.argv) > 3:
	target, keyname = sys.argv[2].split(':')

else:
	target = None
	keyname = None

groupby = field.groupby('geometry', grouping.geometry, target=target, keyname=keyname)

#print([(g[1].slices, g[1].weights.shape) for g in groupby.groups.items()])

outds, outfield = field.apply(groupby, 'total')

if target and keyname:
	outds.attributes['features_src'] = str(target)
	outds.attributes['features_key'] = str(keyname)

if len(sys.argv) > 2:
	ncout = netCDF4Dataset(uri=sys.argv[-1], dataset=outds)
else:
	print('error, no output specified')





