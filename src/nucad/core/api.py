from typing import Union
import cadquery as cq
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from ..error import OCPOperationFailError
from cadquery.occ_impl.geom import BoundBox


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


def check_overlap(
          obj1: Union[TopoDS_Shape, cq.Shape, BoundBox],
          obj2: Union[TopoDS_Shape, cq.Shape, BoundBox]) -> bool:
    if isinstance(obj1, TopoDS_Shape):
        bb_obj1: BoundBox = cq.Shape(obj1).BoundingBox()
    elif isinstance(obj1, cq.Shape):
        bb_obj1: BoundBox = obj1.BoundingBox()
    else:
        bb_obj1: BoundBox = obj1
    
    if isinstance(obj2, TopoDS_Shape):
        bb_obj2: BoundBox = cq.Shape(obj2).BoundingBox()
    elif isinstance(obj2, cq.Shape):
        bb_obj2: BoundBox = obj2.BoundingBox()
    else:
        bb_obj2: BoundBox = obj2

    overlap_x = not (bb_obj1.xmax < bb_obj2.xmin or bb_obj1.xmin > bb_obj2.xmax)
    overlap_y = not (bb_obj1.ymax < bb_obj2.ymin or bb_obj1.ymin > bb_obj2.ymax)
    overlap_z = not (bb_obj1.zmax < bb_obj2.zmin or bb_obj1.zmin > bb_obj2.zmax)
    return overlap_x and overlap_y and overlap_z
