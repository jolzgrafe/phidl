import pytest

from phidl import Device, Layer, LayerSet, make_device, Port
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu

def test_rectangle():
    D = pg.rectangle(size = (4,2), layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '729832d93c8f0c9100ac8fe665894920bc47654a')

def test_bbox():
    D = pg.bbox(bbox = [(-1,-1),(3,4)], layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'e04a2dc0457f4ae300e9d1235fde335362c8b454')

def test_cross():
    D = pg.cross(length = 10, width = 3, layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '18470cb24843265fe42a283f1cde91cbc8a2abe2')

def test_ellipse():
    D = pg.ellipse(radii = (10,5), angle_resolution = 2.5, layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'f46840e01a8b8d292a23d4c651a064d65c563575')

def test_circle():
    D = pg.circle(radius = 10, angle_resolution = 2.5, layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '15a748245d7bdfd4987f081e1494b41096e9c95a')

def test_ring():
    D = pg.ring(radius = 10, width = 0.5, angle_resolution = 2.5, layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '66b57b1544c9c48d9babc107dc93e7b0bf378499')

def test_arc():
    D = pg.arc(radius = 10, width = 0.5, theta = 45, start_angle = 0, angle_resolution = 2.5, layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'a273d16c6c7daf4f80fcdfdd82514be2484d6349')

def test_turn():
    port = Port(name = 1, midpoint = (7.5,6.7), orientation = 47)
    D = pg.turn(port, radius = 10, angle = 270, angle_resolution = 2.5, layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '77dc856a16ed48184b743fe801ce70bedfa82a83')

def test_straight():
    D = pg.straight(size = (4,2), layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '729832d93c8f0c9100ac8fe665894920bc47654a')

def test_L():
    D = pg.L(width = 1, size = (10,20) , layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'fc8e0a442ddc6f348876c14da19fcdaf0024705a')

def test_C():
    D = pg.C(width = 1, size = (10,20) , layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'c021f4b8dc8bcdad6ccc48bd3eb00d2895f7ac98')

def test_offset():
    A = pg.cross(length = 10, width = 3, layer = 0)
    B = pg.ellipse(radii = (10,5), angle_resolution = 2.5, layer = 1)
    D = pg.offset([A,B], distance = 0.1, join_first = True, precision = 0.001, max_points = 4000, layer = 2)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'dea81b4adf9f163577cb4c750342f5f50d4fbb6d')

def test_copy_deepcopy():
    D = Device()
    A = pg.ellipse(radii = (10,5), angle_resolution = 2.5, layer = 1)
    B = pg.ellipse(radii = (10,5), angle_resolution = 2.5, layer = 1)
    a = D << A
    b1 = D << B
    b2 = D << B

    Dcopy = pg.copy(D)
    Ddeepcopy = pg.deepcopy(D)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '0313cd7e58aa265b44dd1ea10265d1088a2f1c6d')
    h = Dcopy.hash_geometry(precision = 1e-4)
    assert(h == '0313cd7e58aa265b44dd1ea10265d1088a2f1c6d')
    h = Ddeepcopy.hash_geometry(precision = 1e-4)
    assert(h == '0313cd7e58aa265b44dd1ea10265d1088a2f1c6d')

    D << pg.ellipse(radii = (12,5), angle_resolution = 2.5, layer = 2)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == '856cedcbbb53312ff839b9fe016996357e658d33')
    h = Dcopy.hash_geometry(precision = 1e-4)
    assert(h == '0313cd7e58aa265b44dd1ea10265d1088a2f1c6d')
    h = Ddeepcopy.hash_geometry(precision = 1e-4)
    assert(h == '0313cd7e58aa265b44dd1ea10265d1088a2f1c6d')

    A.add_ref(pg.ellipse(radii = (12,5), angle_resolution = 2.5, layer = 2))
    B.add_polygon([[3,4,5], [6.7, 8.9, 10.15]], layer = 0)
    h = D.hash_geometry(precision = 1e-4)
    assert(h == 'c007b674e8053c11c877860f0552fff18676b68e')
    h = Dcopy.hash_geometry(precision = 1e-4)
    assert(h == '2590bd786348ab684616eecdfdbcc9735b156e18')
    h = Ddeepcopy.hash_geometry(precision = 1e-4)
    assert(h == '0313cd7e58aa265b44dd1ea10265d1088a2f1c6d')

