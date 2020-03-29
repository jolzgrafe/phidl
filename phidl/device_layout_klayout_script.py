
#%%

import numpy as np
import klayout.db as kdb

# Overview given by https://www.klayout.de/doc-qt5/programming/database_api.html#h2-518

# Create layout aka library
layout = kdb.Layout()

# Create cell https://www.klayout.de/doc-qt5/code/class_Cell.html
kl_cell = layout.create_cell("toplevel")
other_cell = layout.create_cell("toplevel")



# Create polygon
coords = [[1,2],[4,5],[8,3]]
new_poly = kdb.DSimplePolygon([kdb.DPoint(x, y) for x, y in coords])

# Transform polygon
transformation = kdb.CplxTrans(
        1,  # Magnification
        37,  # Rotation
        False,# X-axis mirroring
        10.0, # X-displacement
        20.0  # Y-displacement
        )
new_poly.transform(transformation)



# Create layer https://www.klayout.de/doc-qt5/code/class_Layout.html#m_layer
new_layer = layout.layer(1,6) # new_layer represents the *index* of the relevant layer in the layout's layer list
new_layer2 = layout.layer(3,7) 
new_layer3 = layout.layer(4,8) 
layer_indices = layout.layer_indexes() # Get the layout's indices of layers
layout.layer_infos() # Get the layout's indices of layers
grab_layer = layout.layer(3,7)



# Add polygon to the cell
p1 = kl_cell.shapes(new_layer).insert(new_poly)
p2 = kl_cell.shapes(new_layer).insert(new_poly.transform(transformation))
p3 = kl_cell.shapes(new_layer2).insert(new_poly.transform(transformation))
#shapes = kl_cell.shapes(new_layer)

# Iterate through polygons in one layer of a cell
list(kl_cell.each_shape(new_layer))

# Iterate through all polygons in a cell (get_polygons()) https://www.klayout.de/doc/code/class_Cell.html#method9
all_polygons_iterator = kl_cell.begin_shapes_rec(new_layer)
while not all_polygons_iterator.at_end():
    polygon = all_polygons_iterator.shape()
    print(polygon)
    all_polygons_iterator.next()

# List all layers in use in the entire layout
layers = [(l.layer, l.datatype) for l in layout.layer_infos()]

# List all layers which contain >0 polygons in a cell
layers = []
layer_infos = layout.layer_infos()
for layer_idx in layout.layer_indices():
    kl_iterator = kl_cell.begin_shapes_rec(layer_idx)
    if not kl_iterator.at_end(): # Then there are shapes on that layer
         layers.append( (layer_infos[layer_idx].layer, layer_infos[layer_idx].datatype) )
    
layers = [(l.layer, l.datatype) for l in layout.layer_infos()]    


# Get bounding box of polygon
b = kl_cell.dbbox()
bbox = [[b.left, b.bottom],[b.right, b.top]] 


# Create new cell reference (cell instance) https://www.klayout.de/doc/code/class_CellInstArray.html#method39
ref_cell = other_cell
transformation = kdb.CplxTrans(
        1,  # Magnification
        37,  # Rotation
        False,# X-axis mirroring
        10.0, # X-displacement
        20.0  # Y-displacement
        )
x = kl_cell.insert(kdb.DCellInstArray(ref_cell.cell_index(), transformation, kdb.Vector))
x2 = kl_cell.insert(kdb.DCellInstArray(ref_cell.cell_index(), transformation*transformation))
x3 = kl_cell.insert(kdb.DCellInstArray(ref_cell.cell_index(), transformation*transformation*transformation))

# Iterate through each instance in a cell
for kl_instance in kl_cell.each_inst():
    print(kl_instance)

# Iterate through each polygon in a cell
for kl_polygon in kl_cell.each_shape(0):
    print(kl_polygon)


#%% Notes

# Get child cells: Cell#each_child_cell. 
# Get dependent cells:  Cell#called_cells 
# Get parent cells:  Cell#caller_cells

# Get_polygons in section "Recursive full or region queries" https://www.klayout.de/doc-qt5/programming/database_api.html#h2-907
#layout = RBA::Application::instance.main_window.current_view.active_cellview.layout
## start iterating shapes from cell "TOP", layer index 0
#si = layout.begin_shapes(layout.cell_by_name("TOP"), 0)
#while !si.at_end?
#  puts si.shape.to_s + " with transformation " + si.trans.to_s
#  si.next
#end
    

#%%
import phidl
import phidl.geometry as pg
from phidl import Device, quickplot as qp
import klayout.db as kdb
from phidl.device_layout import DeviceReference, Polygon
from phidl.device_layout import layout
from phidl.device_layout import _parse_layer, _kl_shape_iterator, _get_kl_layer, _objects_to_kl_region

layout.clear()
phidl.reset()

D = Device()
D[1] = D << pg.snspd(layer = 1).rotate(3)
item = D << pg.snspd(layer = 2).rotate(45)
polygon = D.add_polygon([[0,0],[1,2],[5,5]])
item2 = D.add_label('test')



#%%

layout.clear()

#D2 = pg.ellipse(layer = 77)

    def remap_layers(self, layermap = {}, include_labels = True):
        layermap = {_parse_layer(k):_parse_layer(v) for k,v in layermap.items()}


gds_layer, gds_datatype = _parse_layer(layer)
kl_layer_idx, kl_layer =  _get_kl_layer(gds_layer, gds_datatype)
new_gds_layer, new_gds_datatype = _parse_layer(new_layer)
new_kl_layer_idx, new_kl_layer =  _get_kl_layer(new_gds_layer, new_gds_datatype)

if include_labels == True:
    shape_type = kdb.Shapes.SPolygons | kdb.Shapes.STexts
else:
    shape_type = kdb.Shapes.SPolygons

iterator_dict = _kl_shape_iterator(D.kl_cell, shape_type = shape_type, depth = None)
iterator = iterator_dict[kl_layer_idx]
for kl_shape in iterator:
    kl_shape.layer = new_kl_layer_idx
    
    

qp(D)
#%%

return D


#%%

cell_list2 = [cell for cell in layout2.each_cell()]
cell_indices2 = {cell.name: cell.cell_index() for cell in cell_list2}

for i in cell_indices.values():
    layout.rename_cell(i, "")

qp(D3, new_window = True)
#%%
D = Device()
p = D.add_polygon([[1,2],[3,4],[6,9]], layer = (2,3))
p2 = D.add_polygon([[1,2],[3,4],[6,90]])
p3 = D.add_polygon([[1,2,3],[4,6,90]], layer = 7)
#p.rotate(90)

l  = D.add_label('test123', position = [50,0])
print(l.kl_shape)
print(l.kl_text)
l.move([700,7])
print(l.kl_shape)
print(l.kl_text)

D.movex(111)
#D.rotate(45)
print(l.kl_shape)
print(l.kl_text)

kl_shapes = []
for layer_idx in layout.layer_indices():
    kl_shapes += D.kl_cell.each_shape(layer_idx)
print(kl_shapes)
transformation = kdb.DCplxTrans(
    1,
    37,  # Rotation
    False,# X-axis mirroring
    77, # X-displacement
    77,  # Y-displacement
    )

t2 = kdb.DTrans(
    37,  # Rotation
    False,# X-axis mirroring
    77, # X-displacement
    77,  # Y-displacement
    )
x = kl_shapes[3]
[klp.transform(transformation) for klp in kl_shapes]
kl_shapes = []
for layer_idx in layout.layer_indices():
    kl_shapes += D.kl_cell.each_shape(layer_idx)
## Add a text
#kl_text = kdb.DText.new('This is a test', 1.7, 2.9).
#kl_text_shape = D.kl_cell.shapes(0).insert(kl_text)
#kl_text_shape_text = kl_text_shape.dtext


D.kl_cell.write("both.gds")

#%%




#%%
import phidl
import phidl.geometry as pg
from phidl import quickplot as qp
import klayout.db as kdb
from phidl.device_layout import Device

D = pg.rectangle()
D.add_polygon([[0,0],[1,2],[.1,0]], layer = 2)

D.center = [47,47]

qp(D)
#%%

# Get instances

# Transform each instance

# Get polygons

# Transform each polygon


print(d.kl_instance)
transformation = kdb.DCplxTrans(
    float(1),  # Magnification
    float(37),  # Rotation
    False,# X-axis mirroring
    float(0), # X-displacement
    float(0),  # Y-displacement
    )
d.kl_instance.transform(transformation)
print(d.kl_instance)

#%%

import phidl
import phidl.geometry as pg
from phidl import Device, quickplot as qp

R_size = [0.2, 0.2]
nanowire_width = 17
contact_y_setback = 1.5
contact_size = [5,5]
heater_offset_from_middle = 0
nanowire_layer = 240
resistor_layer = 241
resistor_pad_layer = 242


# Calculate sizes
resistor_size = [contact_size[0], contact_y_setback*2 + R_size[1]]
nanowire_y_size_extension = 6
nanowire_size = (nanowire_width, resistor_size[1] + contact_size[1]*2 + nanowire_y_size_extension*2)

# Create devices
D = Device('ktron')
Contact = pg.compass(size = contact_size, layer = {resistor_pad_layer, resistor_layer})
Nanowire = pg.compass(size = nanowire_size, layer = nanowire_layer)

# Coordinates of resistor shape
theta = 45
x1 = R_size[0]/2
x2 = contact_size[0]/2
y1 = R_size[1]/2
y2 = y1 + (x2-x1)*np.tan(theta/180*np.pi)
y3 = y1 +contact_size[1] * np.sin(theta/180*np.pi)#+ contact_y_setback

r = D.add_polygon([(x1,y1), (x2,y2), (x2,y3), (-x2,y3),(-x2,y2),(-x1,y1),
    (-x1,-y1),(-x2,-y2),(-x2,-y3),(x2,-y3),(x2,-y2),(x1,-y1)], layer = resistor_layer)
r.rotate(90)


# Add device references
c_bot = D << Contact
c_top = D << Contact
nw = D << Nanowire

# Move references around
c_top.xmax = r.xmin
c_bot.xmin = r.xmax
c_top.y = r.y
c_bot.y = r.y
# r.xmin = c_top.xmin = c_bot.xmin
# r.ymin = c_bot.ymax
# c_top.ymin = r.ymax
nw.y = r.y
nw.x = r.x - heater_offset_from_middle


D.add_port(port = nw.ports['N'], name = 3)
D.add_port(port = nw.ports['S'], name = 4)
D.add_port(port = c_top.ports['W'], name = 1)
D.add_port(port = c_bot.ports['E'], name = 2)

D.flatten()

qp(D)