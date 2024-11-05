import pya
import numpy as np

def rtpairs(r, n, d):
	for i in range(len(r)):
		for j in range(int(n[i])):    
			yield r[i], j*(2 * np.pi / n[i]), d[i], i
			
app = pya.Application.instance()
mw = app.main_window()
lv = mw.current_view()
ly = lv.active_cellview().layout()
tc = lv.active_cellview().cell
cv_index = lv.active_cellview().cell_index
dbu = ly.dbu
processor = pya.ShapeProcessor()

# Nominal radius of pMUT elements
a = 200
# Proportion of inner electrode radius w.r.t. nominal radius
coverage = 0.8
# Distance between outer ring and flex bondpads
pitch = 10*a
# Total number of rings
rings = 32
# Kerning value for adjacent elements within a ring
kerning_setpoint = 100
# Determines number of elements in a ring
count = np.linspace(0,(rings-1)*10.0,rings)+4 
# Determines ring radii
radii = (kerning_setpoint/2 + a)/np.sin(np.pi/count) 
orientation = np.ones(np.size(radii))

gap = 25 # The spacing between signal rails within a ring [um]
street = 1.8*a # The nominal width of a signal rail [um]

cell_index = ly.add_cell("TOP")
cell = ly.cell(cell_index)

unit_cell_botelectrode = ly.add_cell("pmut$botelectrode")
unit_cell_cavity = ly.add_cell("pmut$cavity")
unit_cell_topelectrode = ly.add_cell("pmut$topelectrode")
cell_botelectrode = ly.cell(unit_cell_botelectrode)
cell_cavity_single = ly.cell(unit_cell_cavity)
cell_topelectrode = ly.cell(unit_cell_topelectrode)
unit_flex_index = ly.cell_by_name("plaus$flexbond$centered")
cell_flex = ly.cell(unit_flex_index)

#Layer definitions
layer_number = 200
layer_info_draft1 = pya.LayerInfo().new(layer_number,0)
layer_index_draft1 = ly.layer(layer_info_draft1)
cell.clear(layer_index_draft1)

layer_number = 201
layer_info_draft2 = pya.LayerInfo().new(layer_number,0)
layer_index_draft2 = ly.layer(layer_info_draft2)
cell.clear(layer_index_draft2)

layer_number = 202
layer_info_draft3 = pya.LayerInfo().new(layer_number,0)
layer_index_draft3 = ly.layer(layer_info_draft3)
cell.clear(layer_index_draft3)

layer_number = 203
layer_info_draft4 = pya.LayerInfo().new(layer_number,0)
layer_index_draft4 = ly.layer(layer_info_draft4)
cell.clear(layer_index_draft4)

layer_number = 204
layer_info_draft5 = pya.LayerInfo().new(layer_number,0)
layer_index_draft5 = ly.layer(layer_info_draft5)
cell.clear(layer_index_draft5)

layer_number = 44
layer_info_mask = pya.LayerInfo(layer_number,0)
layer_index_mask = ly.layer(layer_info_mask)

layer_number = 40
layer_info_M1 = pya.LayerInfo(layer_number,0)
layer_index_M1 = ly.layer(layer_info_M1)

layer_number = 43
layer_info_M2 = pya.LayerInfo(layer_number,0)
layer_index_M2 = ly.layer(layer_info_M2)

layer_number = 42
layer_info_VIA = pya.LayerInfo(layer_number,0)
layer_index_VIA = ly.layer(layer_info_VIA)

# Creation of a discrete pMUT cell
Circle = pya.Polygon.ellipse(pya.Box().new(-a/dbu,-a/dbu,a/dbu,a/dbu),48)
Rectangle = pya.Box().new(-15/dbu,-1.1*street/dbu,15/dbu,1.1*street/dbu)
Vent = pya.Polygon.new(Rectangle)
cell_cavity_single.shapes(layer_index_mask).insert(Circle)
cell_cavity_single.shapes(layer_index_draft5).insert(Vent)
Circle = pya.Polygon.ellipse(pya.Box().new(-coverage*a/dbu,-coverage*a/dbu,coverage*a/dbu,coverage*a/dbu),48)
cell_botelectrode.shapes(layer_index_M1).insert(Circle)
Circle = pya.Polygon.ellipse(pya.Box().new(-coverage*a/dbu,-coverage*a/dbu,coverage*a/dbu,coverage*a/dbu),48)
cell_topelectrode.shapes(layer_index_M2).insert(Circle)

cell_flexleads_index = ly.add_cell("flexleads")
cell_flexleads = ly.cell(cell_flexleads_index)

array_flexleads_index = ly.add_cell("array$flexleads")
array_flexleads = ly.cell(array_flexleads_index)

# Design factor for increasing flex lead width towards outer rings
exponent = 1.25 
width_unit = 50 # Base flex lead width in [um]
spacing = 50 # Spacing between adjacent flex leads in [um]

# Create flexleads
width = [width_unit]
Y = [0.5*(width_unit+spacing)]
terminus = radii[rings-1]+street
X = []
i = 0
for i in range(rings):
	if i == 0:
		x1 = (radii[i]+0.5*street)*np.cos(np.arcsin(Y[i]/(radii[i]+0.5*street)))
		x2 = (radii[i]+0.5*street)*np.cos(np.arcsin(Y[i]/(radii[i]+0.5*street)))
	else:
		x1 = (radii[i]+0.5*street)*np.cos(np.arcsin(Y[i]/(radii[i]+0.5*street)))
		x2 = (radii[i]-0.5*street)*np.cos(np.arcsin(Y[i]/(radii[i]-0.5*street)))
	X1 = (terminus)*np.cos(np.arcsin(Y[i]/(terminus)))
	X2 = X1
	X.append(X1)
	start2 = pya.Point.new(x2/dbu,-Y[i]/dbu)
	end2 = pya.Point.new(X2/dbu,-Y[i]/dbu)
	path2 = pya.Path.new([start2,end2],(width[i])/dbu)
	cell_flexleads.shapes(layer_index_draft4).insert(path2)
	start1 = pya.Point.new(x1/dbu,Y[i]/dbu)
	end1 = pya.Point.new(X1/dbu,Y[i]/dbu)
	path1 = pya.Path.new([start1,end1],(width[i])/dbu)
	cell_flexleads.shapes(layer_index_draft4).insert(path1)
	i = i + 1
	width.append(width_unit+i**exponent)
	Y.append(Y[i-1]+(width[i]+width[i-1])/2+spacing)
	
cell_flexmask_index = ly.add_cell("flexmask")
cell_flexmask = ly.cell(cell_flexmask_index)
array_flexmask_index = ly.add_cell("array$flexmask")
array_flexmask = ly.cell(array_flexmask_index)

i = i + 1
width.append(50+i**exponent)
Y.append(Y[i-1]+(width[i]+width[i-1])/2+spacing)
radii = np.append(radii,radii[rings-1]+pitch)
radii = np.append(radii,radii[rings]+pitch)

for i in range(rings+1):
	if i == 0:
		mask1 = [pya.Point.new(0.5*(radii[i]+radii[i+1])/dbu,0),pya.Point.new(0.5*(radii[i]+radii[i+1])*np.cos(np.arcsin(2*(Y[i+1]-width[i+1]*0.5)/(radii[i]+radii[i+1])))/dbu,   (Y[i+1]-width[i+1]*0.5)/dbu)]
		mask2 = [pya.Point.new(0.5*(radii[i]+radii[i+1])/dbu,0),pya.Point.new(0.5*(radii[i]+radii[i+1])*np.cos(np.arcsin(2*(Y[i+1]-width[i+1]*0.5)/(radii[i]+radii[i+1])))/dbu,    -(Y[i+1]-width[i+1]*0.5)/dbu)]
	elif i < rings:
		mask1.append(pya.Point.new(((0.5*(radii[i]+radii[i+1]))*np.cos(np.arcsin((Y[i]-width[i]*0.5)/(0.5*(radii[i]+radii[i+1])))))/dbu,(Y[i]-width[i]*0.5)/dbu))
		mask1.append(pya.Point.new(((0.5*(radii[i]+radii[i+1]))*np.cos(np.arcsin((Y[i+1]-width[i+1]*0.5)/(0.5*(radii[i]+radii[i+1])))))/dbu,(Y[i+1]-width[i+1]*0.5)/dbu))
		mask2.append(pya.Point.new(radii[i]*np.cos(np.arcsin((Y[i]-width[i]*0.5)/radii[i]))/dbu,-(Y[i]-width[i]*0.5)/dbu))
		mask2.append(pya.Point.new(radii[i]*np.cos(np.arcsin((Y[i+1]-width[i+1]*0.5)/radii[i]))/dbu,-(Y[i+1]-width[i+1]*0.5)/dbu))
	else:
		mask1.append(pya.Point.new(((0.5*(radii[i]+radii[i+1]))*np.cos(np.arcsin((Y[i]-width[i]*0.5)/(0.5*(radii[i]+radii[i+1])))))/dbu,(Y[i]-width[i]*0.5)/dbu))
		mask2.append(pya.Point.new(radii[i]*np.cos(np.arcsin((Y[i]-width[i]*0.5)/radii[i]))/dbu,-(Y[i]-width[i]*0.5)/dbu))

mask1.append(pya.Point.new(((1.0*(radii[i]+radii[i+1]))*np.cos(np.arcsin((Y[i]-width[i]*0.5)/(0.5*(radii[i]+radii[i+1])))))/dbu,0))
mask2.append(pya.Point.new(1.5*radii[i]*np.cos(np.arcsin((Y[i]-width[i]*0.5)/radii[i]))/dbu,0))
poly1 = pya.Polygon.new(mask1)
poly2 = pya.Polygon.new(mask2)
cell_flexmask.shapes(layer_index_draft3).insert(poly1)
cell_flexmask.shapes(layer_index_draft3).insert(poly2)

for i in range(4):
trans = pya.ICplxTrans().new(1.0,i*90,False,0,0)
array_flexleads.insert(pya.CellInstArray().new(cell_flexleads_index, trans))
array_flexmask.insert(pya.CellInstArray().new(cell_flexmask_index, trans))
array_flexleads.flatten(False)
array_flexmask.flatten(False)

botelectrode_index = ly.add_cell("array$botelectrode")
cell_botelectrode = ly.cell(botelectrode_index)
topelectrode_index = ly.add_cell("array$topelectrode")
cell_topelectrode = ly.cell(topelectrode_index)
cavity_index = ly.add_cell("array$cavity")
cell_cavity = ly.cell(cavity_index)
mask_index = ly.add_cell("array$mask")
cell_mask = ly.cell(mask_index)

# Create array of pMUT elements
for r, t, d, i in rtpairs(radii[0:rings], count[0:rings], orientation):
	dx = r * np.cos(t)
	dy = r * np.sin(t)
	dt = np.rad2deg(t)
	trans = pya.ICplxTrans().new(1.0, dt-d*90, False, dx/dbu, dy/dbu)
	if ((((dy - a) > Y[i+1]-0.5*width[i+1] or (dy + a) < -Y[i+1]+0.5*width[i+1])) and (abs(dy) <= abs(dx))) or ((((dx - a) > Y[i+1]-0.5*width[i+1] or (dx + a) < -Y[i+1]+0.5*width[i+1])) and (abs(dx) <= abs(dy))) or (i == 0):
		cell_botelectrode.insert(pya.CellInstArray().new(unit_cell_botelectrode, trans))
		cell_topelectrode.insert(pya.CellInstArray().new(unit_cell_topelectrode, trans))
		cell_mask.insert(pya.CellInstArray().new(unit_cell_cavity, trans))
	cell_cavity.insert(pya.CellInstArray().new(unit_cell_cavity, trans))
	
# Create piezo cutout mask
release_index = ly.add_cell("array$release")
cell_release = ly.cell(release_index)
mask_radius = (radii[rings-1]+0.6*pitch)/dbu
mask_circle = pya.Polygon.ellipse(pya.Box().new(-mask_radius,-mask_radius,mask_radius,mask_radius),128)
cell_release.shapes(layer_index_draft1).insert(mask_circle)
processor.boolean(ly,cell_release,layer_index_draft1,ly,cell_mask,layer_index_mask,cell.shapes(layer_index_VIA),pya.EdgeProcessor.ModeANotB, True,True,True)

# Donut Creation 
def create_donut(outer_radius,inner_radius,layer_index,cell):
	OuterCircle = pya.Polygon.ellipse(pya.Box().new(-outer_radius/dbu,-outer_radius/dbu,outer_radius/dbu,outer_radius/dbu),128)
	InnerCircle = pya.Polygon.ellipse(pya.Box().new(-inner_radius/dbu,-inner_radius/dbu,inner_radius/dbu,inner_radius/dbu),128)
	Donut = pya.Region().new(OuterCircle) - pya.Region().new(InnerCircle)
	cell.shapes(layer_index).insert(Donut)

for i in range(rings):
	if radii[i] != 0:
		if i != 0:
			create_donut(radii[i] - gap, radii[i] - street, layer_index_draft1,cell_botelectrode)
			create_donut(radii[i] - gap, radii[i] - street, layer_index_draft1,cell_topelectrode)
			create_donut(radii[i] + street, radii[i] + gap, layer_index_draft2,cell_topelectrode)
			create_donut(radii[i] + street, radii[i] + gap, layer_index_draft2,cell_botelectrode)
		if i + 1 < np.size(radii):
			create_donut(radii[i+1] - street, radii[i] + street, layer_index_mask,cell_cavity)
		else:
			create_donut(radii[i] +pitch - street, radii[i] + street, layer_index_mask,cell_cavity)

# Create center electrode pie
cell_center_index = ly.add_cell("center")
cell_center = ly.cell(cell_center_index)
array_center_index = ly.add_cell("array$center")
array_center = ly.cell(array_center_index)

n = 40
r = (radii[0]+street)/dbu
da = np.pi/n
angle_gap = np.arctan(gap/(r*dbu))
angle_start = angle_gap
angle_end = np.pi/4-angle_gap
angles = np.linspace(angle_start,angle_end,n/4)

mask = [pya.Point.new(gap/np.arcsin(np.pi/8)*np.cos(np.pi/8)/dbu,gap/dbu)]
for a in angles:
	mask.append(pya.Point.new(r*np.cos(a),r*np.sin(a)))
poly = pya.Polygon.new(mask)
cell_center.shapes(layer_index_draft1).insert(poly)

angle_start = -angle_gap
angle_end = -np.pi/4+angle_gap
angles = np.linspace(angle_start,angle_end,n/4)

mask = [pya.Point.new(gap/np.arcsin(np.pi/8)*np.cos(np.pi/8)/dbu,-gap/dbu)]
for a in angles:
	mask.append(pya.Point.new(r*np.cos(a),r*np.sin(a)))
poly = pya.Polygon.new(mask)
cell_center.shapes(layer_index_draft2).insert(poly)

processor.boolean(ly,cell_center,layer_index_draft1,ly,cell_mask,layer_index_mask,cell_center.shapes(layer_index_M2),pya.EdgeProcessor.ModeANotB, True,True,True)
processor.boolean(ly,cell_center,layer_index_draft2,ly,cell_mask,layer_index_mask,cell_center.shapes(layer_index_M1),pya.EdgeProcessor.ModeANotB, True,True,True)
cell_center.copy(layer_index_draft1,layer_index_M1)
cell_center.copy(layer_index_draft2,layer_index_M2)

for i in range(4):
	trans = pya.ICplxTrans().new(1.0,i*90,False,0,0)
	array_center.insert(pya.CellInstArray().new(cell_center_index, trans))
	
# Donut masking
processor.boolean(ly,cell_botelectrode,layer_index_draft1,ly,cell_mask,layer_index_mask,cell_botelectrode.shapes(layer_index_M1),pya.EdgeProcessor.ModeANotB, True,True,True)
processor.boolean(ly,cell_topelectrode,layer_index_draft2,ly,cell_mask,layer_index_mask,cell_topelectrode.shapes(layer_index_M2),pya.EdgeProcessor.ModeANotB, True,True,True)
cell_botelectrode.copy(layer_index_draft2,layer_index_M1)
cell_topelectrode.copy(layer_index_draft1,layer_index_M2)


# Donut cutout leads
processor.boolean(ly,cell_botelectrode,layer_index_M1,ly,array_flexmask,layer_index_draft3,cell_botelectrode.shapes(layer_index_M1),pya.EdgeProcessor.ModeANotB, True,True,True)
processor.boolean(ly,cell_topelectrode,layer_index_M2,ly,array_flexmask,layer_index_draft3,cell_topelectrode.shapes(layer_index_M2),pya.EdgeProcessor.ModeANotB, True,True,True)
cell_botelectrode.copy(array_flexleads,layer_index_draft4,layer_index_M1)
cell_topelectrode.copy(array_flexleads,layer_index_draft4,layer_index_M2)

# Merge vent holes with cavity
cell_cavity_single.copy(layer_index_draft5,layer_index_mask)

# Merge all cells
trans = pya.ICplxTrans().new(0,0)

cell.insert(pya.CellInstArray().new(cell_flexmask_index, trans))
cell.insert(pya.CellInstArray().new(botelectrode_index, trans))
cell.insert(pya.CellInstArray().new(topelectrode_index, trans))
cell.insert(pya.CellInstArray().new(cavity_index, trans))
cell.insert(pya.CellInstArray().new(array_center_index, trans))

# Insert flex pads
offset = (radii[rings]+2240)/dbu
x = [offset,0,-offset,0]
y = [0,-offset,0,offset]
a = [90,0,-90,180]

x1 = [radii[rings-1], (-14580/2), -radii[rings-1]-2240, (-14580/2)]
y1 = [(-14580/2), -radii[rings-1]-2240, (-14580/2), radii[rings-1]]
x2 = [radii[rings-1]+2240, (14580/2), -radii[rings-1], (14580/2)]
y2 = [(14580/2), -radii[rings-1], (14580/2), radii[rings-1]+2240]

i1 = [np.ceil(radii[rings-1]+a+street)[0],(15580/2), -np.ceil(radii[rings-1]+a+street)[0]-5000, (-15580/2)]
j1 = [(15580/2), -np.ceil(radii[rings-1]+a+street)[0]-5000, (-15580/2), np.ceil(radii[rings-1]+a+street)[0]]
i2 = [np.ceil(radii[rings-1]+a+street)[0]+5000, (18580/2), -np.ceil(radii[rings-1]+a+street)[0], (-18580/2)]
j2 = [(18580/2), -np.ceil(radii[rings-1]+a+street)[0], (-18580/2), np.ceil(radii[rings-1]+a+street)[0]+5000]

a1 = [np.ceil(radii[rings-1]+a+street)[0],(15580/2), -np.ceil(radii[rings-1]+a+street)[0]-300, (-15580/2)]
b1 = [(15580/2), -np.ceil(radii[rings-1]+a+street)[0]-300, (-15580/2), np.ceil(radii[rings-1]+a+street)[0]]
a2 = [np.ceil(radii[rings-1]+a+street)[0]+300, (-15580/2), -np.ceil(radii[rings-1]+a+street)[0], (15580/2)]
b2 = [(-15580/2), -np.ceil(radii[rings-1]+a+street)[0], (15580/2), np.ceil(radii[rings-1]+a+street)[0]+300]

for i in range(4):
	trans = pya.ICplxTrans().new(1.0,a[i],False,x[i],y[i])
	cell.insert(pya.CellInstArray().new(unit_flex_index, trans))
	cell.shapes(layer_index_VIA).insert(pya.Box().new(x1[i]/dbu,y1[i]/dbu,x2[i]/dbu,y2[i]/dbu))
	cell.shapes(layer_index_mask).insert(pya.Box().new(i1[i]/dbu,j1[i]/dbu,i2[i]/dbu,j2[i]/dbu))
	cell.shapes(layer_index_mask).insert(pya.Box().new(-i1[i]/dbu,j1[i]/dbu,-i2[i]/dbu,j2[i]/dbu))
	cell.shapes(layer_index_mask).insert(pya.Box().new(a1[i]/dbu,b1[i]/dbu,a2[i]/dbu,b2[i]/dbu))
	
cell.clear(layer_index_draft1)
cell.clear(layer_index_draft2)
cell.clear(layer_index_draft3)
cell.clear(layer_index_draft4)

# Insert flex traces
cell_trace_index = ly.add_cell("trace")
cell_trace = ly.cell(cell_trace_index)
array_trace_index = ly.add_cell("array$trace")
array_trace = ly.cell(array_trace_index)

for i in range(rings):
	trace = []
	trace.append(pya.Point.new(X[i]/dbu,(Y[i]+0.5*width[i])/dbu))
	trace.append(pya.Point.new(X[i]/dbu,(Y[i]-0.5*width[i])/dbu))
	trace.append(pya.Point.new(offset-2230/dbu,(200*i+20)/dbu))
	trace.append(pya.Point.new(offset-2230/dbu,(200*i+180)/dbu))
	poly = pya.Polygon.new(trace)
	cell_trace.shapes(layer_index_draft1).insert(poly)
	
	trace = []
	trace.append(pya.Point.new(X[i]/dbu,-(Y[i]+0.5*width[i])/dbu))
	trace.append(pya.Point.new(X[i]/dbu,-(Y[i]-0.5*width[i])/dbu))
	trace.append(pya.Point.new(offset-2230/dbu,-(200*i+20)/dbu))
	trace.append(pya.Point.new(offset-2230/dbu,-(200*i+180)/dbu))
	poly = pya.Polygon.new(trace)
	cell_trace.shapes(layer_index_draft1).insert(poly)
	
cell_trace.copy(layer_index_draft1,layer_index_M1)
cell_trace.copy(layer_index_draft1,layer_index_M2)

for i in range(4):
	trans = pya.ICplxTrans().new(1.0,a[i],False,0,0)
	array_trace.insert(pya.CellInstArray().new(cell_trace_index, trans))

trans = pya.ICplxTrans().new(0,0)
cell.insert(pya.CellInstArray().new(array_trace_index, trans))
