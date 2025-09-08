from typing import List, Optional, overload
import pycatima as catima
import logging

from ..types import CATIMA_Material, CATIMA_Layers
from .track import TrackIntersection


logger = logging.getLogger(__name__)


class Materials(object):
    def __init__(self, intersection: Optional[List[TrackIntersection]] = None):
        self.names: List[str] = []
        self.layers: CATIMA_Layers = catima.Layers() # type: ignore
        
        if intersection is not None:
            for x in intersection:
                name = x.object.name
                if 'material' in x.object.metadata:
                    mat = x.object.metadata['material']
                    thickness = x.edge.Length() # type: ignore
                    mat.thickness_cm(thickness * 1e-1) # mm->cm
                    self.add(name, mat)
                else:
                    logger.info(f'ignore {x.object.name} because the object does not contain material in metadata.')


    def size(self) -> int:
        return self.layers.num()


    def __len__(self) -> int:
        return self.size()


    def __sizeof__(self) -> int:
        return self.size()


    def add(self, name: str, material: CATIMA_Material):
        self.names.append(name)
        self.layers.add(material)


    @overload
    def get(self, key: str):
        ...


    @overload
    def get(self, key: int):
        ...


    def get(self, key):
        if isinstance(key, int):
            idx = key
        elif isinstance(key, str):
            if key in self.names:
                idx = self.names.index(key)
            else:
                raise KeyError(f'{key} not found')
        else:
            raise TypeError
        return self.layers.get(idx)

