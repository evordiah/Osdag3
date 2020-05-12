'''
Created on 27-May-2015

@author: deepa
'''
import numpy
from cad.items.ModelUtils import getGpPt, makeEdgesFromPoints, makeWireFromEdges, makeFaceFromWire, makePrismFromFace

'''

                        ^   a2 X
                        |      | X
                        |      |   X
                        |      |     X
                        |      |       X
                        +      |         X
                        h      |           X
                        +      |             X
                        |      |               X
                        |      |                 X
                        v   a1 +-------------------X a3


                               <------- b --------->


'''
class FilletWeld(object):

    def __init__(self, b, h, L):
        self.L = L
        self.b = b
        self.h = h
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin
        self.a2 = self.sec_origin + self.b * self.uDir
        self.a3 = self.sec_origin + self.h * self.vDir
        self.points = [self.a1, self.a2, self.a3]

    def create_model(self):
        Pnt = getGpPt(self.sec_origin)
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * (self.wDir)  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
        return prism


if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()
    from OCC.gp import gp_Pnt

    b = 10
    h = 10
    L = 50

    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([0., 0., 1.])
    shaftDir = numpy.array([0., 1., 0.])

    FWeld = FilletWeld(b, h, L)
    _place = FWeld.place(origin, uDir, shaftDir)
    point = FWeld.compute_params()
    prism = FWeld.create_model()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
