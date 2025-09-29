from abc import abstractmethod
from typing import Dict, List, Optional, Any
import cadquery as cq
import logging

from ..types import Real, Vector3
from ..core.track import Track, TrackIntersection, intersect_assembly_track
from ..core.util import get_components
from ..core.material import MaterialLike

logger = logging.getLogger(__name__)


def make_metadata(
    material: Optional[MaterialLike] = None
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


    def intersect_track(self, track: Track, l: Real = 10e3) ->  List[TrackIntersection]:
        return intersect_assembly_track(self.setup, track, l)
    

    def components(self) -> Dict[str, cq.Assembly]:
        return get_components(self.setup)



