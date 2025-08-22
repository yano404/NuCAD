from abc import abstractmethod
from typing import Dict, List, Optional, Any, Tuple
import cadquery as cq
from OCP.gp import gp_Pnt
import pycatima as catima
import logging

from ..types import CATIMA_Layers, CATIMA_Material, Vector3
from ..error import InvalidGeometryError
from ..util.cqutil import get_components, intersection, get_line_endpoints, find_intersection_assembly_line, find_obj_containing_pnt
    

logger = logging.getLogger(__name__)


def make_metadata(
    material: Optional[CATIMA_Material] = None
):
    metadata = {}
    if material:
        metadata['material'] = material
    return metadata


class SetupBase(object):
    def __init__(
        self,
        name: Optional[str] = None,
        origin: Vector3 = (0.0, 0.0, 0.0),
        normal: Vector3 = (0.0, 0.0, 1.0),
        xDir: Vector3 = (1.0, 0.0, 0.0),
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.setup = cq.Assembly(
            name = name,
            metadata = metadata)
        self.construct(
            origin = origin,
            normal = normal,
            xDir = xDir
        )

    @abstractmethod
    def construct(
        self,
        origin: Vector3 = (0.0, 0.0, 0.0),
        normal: Vector3 = (0.0, 0.0, 1.0),
        xDir: Vector3 = (1.0, 0.0, 0.0)
    ):
        '''
        example

        self.setup.add(
            cq.Workplane().box(100, 100, 100),
            name='box',
            metadata=make_metadata(material=gagg)
        )
        '''
        pass


    def add(self, *args, **kwargs):
        self.setup.add(*args, **kwargs)


    def find_intersection_line(self, line: cq.Workplane):
        return find_intersection_assembly_line(self.setup, line)
    

    def find_obj_containing_pnt(self, pnt: gp_Pnt):
        return find_obj_containing_pnt(self.setup, pnt)

    
    def make_catima_layers(self, line: cq.Workplane) -> Tuple[List[str], CATIMA_Layers]:
        names = []
        lys = catima.Layers() # type: ignore

        pnt0, pnt1 = get_line_endpoints(line)
        obj_p0_list = self.find_obj_containing_pnt(pnt0)
        obj_p1_list = self.find_obj_containing_pnt(pnt1)
        if len(obj_p0_list) > 1:
            raise InvalidGeometryError(
                f'{[o.name for o in obj_p0_list]} share the endpoint of the vertex'
            )
        
        if len(obj_p1_list) > 1:
            raise InvalidGeometryError(
                f'{[o.name for o in obj_p1_list]} share the endpoint of the vertex'
            )
        
        intersections = self.find_intersection_line(line)

        if obj_p0_list:
            obj_p0 = obj_p0_list[0]
            intersections.insert(
                0,
                intersection(pnt0, obj_p0, line)
            )
        
        if obj_p1_list:
            obj_p1 = obj_p1_list[0]
            intersections.append(
                intersection(pnt1, obj_p1, line)
            )

        for i in range(0, len(intersections), 2):
            int0 = intersections[i]
            int1 = intersections[i+1]

            if int0.object is not int1.object:
                raise InvalidGeometryError(
                    f'points are not shared by the same object'
                )
            
            thickness = int1.pnt.Distance(int0.pnt)
            
            if 'material' in int0.object.metadata:
                mat = int0.object.metadata['material']
                mat.thickness_cm(thickness * 1e-1) # mm->cm
                lys.add(mat)
                names.append(int0.object.name)
            else:
                logger.info(f'ignore {int0.object.name} because the object does not contain material in metadata.')
        
        return (names, lys)
    

    def components(self) -> Dict[str, cq.Assembly]:
        return get_components(self.setup)



