from typing import overload
import cadquery as cq
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from numpy import isin
from ..error import OCPOperationFailError


def intersect(obj1: TopoDS_Shape, obj2: TopoDS_Shape) -> cq.Shape:
    com = BRepAlgoAPI_Common(obj1, obj2)
    com.Build()
    if not com.IsDone():
        raise OCPOperationFailError('failed to calculate the intersection')
    return cq.Shape(com.Shape())


def subtract():
    ...


def union():
    ...

