from abc import abstractmethod
from typing import Dict, List, Optional, Any, Self
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
        *args,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        self.setup = cq.Assembly(
            name = name,
            metadata = metadata)
        self.construct(
            *args,
            **kwargs
        )

    @abstractmethod
    def construct(
        self,
        *args,
        **kwargs
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


    def add(self, obj: cq.Assembly | cq.Workplane | Self, *args, **kwargs):
        if isinstance(obj, SetupBase):
            self.setup.add(obj.setup, *args, **kwargs)
        else:
            self.setup.add(obj, *args, **kwargs)

    def intersect_track(self, track: Track, l: Real = 10e3) ->  List[TrackIntersection]:
        return intersect_assembly_track(self.setup, track, l)
    

    def components(self) -> Dict[str, cq.Assembly]:
        return get_components(self.setup)



