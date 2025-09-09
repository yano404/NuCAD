from typing import List
import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from .geometry import Pnt, Dir, Lin
from .api import intersect
from ..types import Real, Vector3
from cadquery.occ_impl.geom import BoundBox


class Track(object):
    def __init__(self, origin: Vector3, dir: Vector3, local: cq.Plane = cq.Plane((0,0,0), normal = (0,0,1))):
        self.origin: Pnt = Pnt(*origin)
        self.dir: Dir = Dir(*dir)
        self.line = Lin(self.origin, self.dir)
        self.local = local


    def local_xy(self, z: Real) -> cq.Vector:
        return cq.Vector(self.origin) + (z - self.origin.Z()) * cq.Vector(self.dir)


    def make_edge_local(self, l: Real) -> cq.Edge:
        return cq.Edge(BRepBuilderAPI_MakeEdge(self.line, 0, l).Edge())


    def make_edge(self, l: Real) -> cq.Shape:
        return self.make_edge_local(l).transformShape(self.local.rG)


class TrackIntersection(object):
    def __init__(
            self,
            edge: cq.Shape,
            track: Track,
            object: cq.Assembly
        ) -> None:
        self.edge: cq.Shape = edge
        self.track: Track = track
        self.object: cq.Assembly = object
        self.dist: Real = self.edge.Center().toPnt().Distance(
            self.track.origin
        )
        
    
    def __lt__(self, other):
        return self.dist < other.dist
    
    
    def __gt__(self, other):
        return self.dist > other.dist


def intersect_assembly_track(
        assembly: cq.Assembly,
        track: Track,
        l: Real) ->  List[TrackIntersection]:
    results: List[TrackIntersection] = []
    edge = track.make_edge(l)
    bb_edge: BoundBox = edge.BoundingBox()
    for x in assembly.children:
        if x.children:
            results.extend(
                intersect_assembly_track(x, track, l)
            )
        else:
            obj = x.obj.toOCC() # type: ignore
            bb_obj: BoundBox = cq.Shape(obj).BoundingBox()
            overlap_x = not (bb_edge.xmax < bb_obj.xmin or bb_edge.xmin > bb_obj.xmax)
            overlap_y = not (bb_edge.ymax < bb_obj.ymin or bb_edge.ymin > bb_obj.ymax)
            overlap_z = not (bb_edge.zmax < bb_obj.zmin or bb_edge.zmin > bb_obj.zmax)
            overlap = overlap_x and overlap_y and overlap_z
            if overlap:
                intersection_shape = intersect(
                    obj,
                    edge.wrapped
                )
                for e in intersection_shape.Edges():
                    results.append(TrackIntersection(
                        e,
                        track,
                        x
                    ))
    results.sort()
    return results
