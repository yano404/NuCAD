from typing import List, Union, Tuple
import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from .geometry import Pnt, Dir, Lin
from .api import check_overlap, intersect
from ..types import Real, Vector3
from .util import get_components, get_object
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

    for x in get_components(assembly).values():
        obj = get_object(x, coord='world').wrapped
        if check_overlap(bb_edge, obj):
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
