from typing import Dict, List
import numpy as np
import cadquery as cq
from cadquery.occ_impl.shapes import Edge, Vertex
from cadquery.assembly import AssemblyObjects
from OCP.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCP.BRepIntCurveSurface import BRepIntCurveSurface_Inter
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.TopoDS import TopoDS_Solid, TopoDS_Edge, TopoDS_Shape
from OCP.TopAbs import TopAbs_State

from ..types import Real, Vector3
from ..error import OCPOperationFailError


IN = TopAbs_State.TopAbs_IN
ON = TopAbs_State.TopAbs_ON
OUT = TopAbs_State.TopAbs_OUT


def get_line_endpoints(line: cq.Workplane):
    edge: Edge = line.val() # type: ignore
    vertices: List[Vertex] = edge.Vertices()
    pnt0: gp_Pnt = gp_Pnt(*vertices[0].toTuple())
    pnt1: gp_Pnt = gp_Pnt(*vertices[1].toTuple())
    return pnt0, pnt1

class intersection(object):
    pnt: gp_Pnt
    object: cq.Assembly
    line: cq.Workplane
    dist: Real

    def __init__(
        self,
        pnt: gp_Pnt,
        object: cq.Assembly,
        line: cq.Workplane
    ):
        self.pnt = pnt
        self.object = object
        self.line = line

        pnt0, pnt1 = get_line_endpoints(line)
        self.dist = self.pnt.Distance(pnt0)
    
    def __lt__(self, other):
        return self.dist < other.dist
    
    def __gt__(self, other):
        return self.dist > other.dist


def boolean_edge_solid(edge: TopoDS_Edge, solid: TopoDS_Solid) -> TopoDS_Shape:
    com = BRepAlgoAPI_Common(solid, edge)
    com.Build()
    if not com.IsDone():
        raise OCPOperationFailError(f'Failed to calculate the common parts between {edge} and {solid} with BRepAlgoAPI_Common')
    return com.Shape()


def find_intersection_object_line(
    obj: AssemblyObjects,
    line: cq.Workplane,
    tol: float = 1e-7
) -> List[gp_Pnt]:
    pnt0, pnt1 = get_line_endpoints(line)
    vec = gp_Vec(pnt0, pnt1)
    len_vec = vec.Magnitude()

    lin = gp_Lin(pnt0, gp_Dir(vec))

    intersector = BRepIntCurveSurface_Inter()
    intersector.Init(obj.toOCC(), lin, tol) # type: ignore

    intersections = []

    while intersector.More():
        pnt_int = intersector.Pnt()
        vec_int = gp_Vec(pnt0, pnt_int)
        proj = vec_int.Dot(vec) / len_vec
        if  -tol < proj < len_vec + tol:
            intersections.append(pnt_int)
        intersector.Next()

    return intersections


def find_intersection_assembly_line(
    assembly: cq.Assembly,
    line: cq.Workplane
) -> List[intersection]:
    results = []
    for x in assembly.children:
        if x.children:
            results.extend(find_intersection_assembly_line(x, line))
        else:
            pnts = find_intersection_object_line(x.obj, line)
            for pnt in pnts:
                results.append(intersection(pnt, x, line))
    results.sort()
    return results


def is_pnt_inside_solid(
        pnt: gp_Pnt,
        solid: cq.Workplane,
        tol: Real = 1e-7
    ) -> TopAbs_State:
    topods_solid: TopoDS_Solid = solid.toOCC()
    classifier = BRepClass3d_SolidClassifier(
        topods_solid,
        pnt,
        tol
    )
    return classifier.State()


def find_obj_containing_pnt(
    assembly: cq.Assembly,
    pnt: gp_Pnt
) -> List[cq.Assembly]:
    results = []
    for x in assembly.children:
        if x.children:
            results.extend(find_obj_containing_pnt(x, pnt))
        else:
            if is_pnt_inside_solid(pnt, x.obj) == IN: # type: ignore
                results.append(x)
    return results


def get_components(assembly: cq.Assembly) -> Dict[str, cq.Assembly]:
        results = {}
        for x in assembly.children:
            if x.children:
                results.update(get_components(x))
            else:
                results[x.name] = x
        return results