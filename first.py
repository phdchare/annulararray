import pya
import numpy as np

def rtpairs(r, n, d):
	for i in range(len(r)):
		for j in range(n[i]):    
			yield r[i], j*(2*np.pi/n[i]), d[i]

app = pya.Application.instance()
mw = app.main_window()
lv = mw.current_view()
ly = lv.active_cellview().layout()
tc = lv.active_cellview().cell
cv_index = lv.active_cellview().cell_index
dbu = ly.dbu

# Radius of a pMUT element
a = 300
# Parameter value for determining ring radii
pitch = 4*a
# List of ring radii
radii = np.array([0.45,1.1,2,3,4,5,6,7,8,9,10,11])*pitch
# List of element count per ring
count = np.array([4,10,20,30,40,50,60,66,66,66,66,66])
orientation = np.array([-1,1,1,1,1,1,1,1,1,1,1,1])

layer_number = 1
datatype = 0
layer_info = pya.LayerInfo().new(layer_number,datatype)
layer_index = ly.layer(layer_info)

cell_index = ly.add_cell("ANNULAR_ARRAY")
cell = ly.cell(cell_index)

# A pre-made cell consisting of a discrete pMUT
unit_cell_index = ly.cell_by_name("PMUT")
unit_cell = ly.cell(unit_cell_index)

for r, t, d in rtpairs(radii, count, orientation):
	dx = r * np.cos(t)
	dy = r * np.sin(t)
	dt = np.rad2deg(t)
	trans = pya.ICplxTrans().new(1.0,dt-d*90,False,dx/dbu,dy/dbu)
	cell.insert(pya.CellInstArray().new(unit_cell_index,trans))
