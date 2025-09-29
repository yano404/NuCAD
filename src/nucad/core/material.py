from typing import NewType, List, Optional, Union, overload
import pycatima as catima
import logging

from ..types import Real
from .track import TrackIntersection


logger = logging.getLogger(__name__)


class Material(catima.Material): # type: ignore
    def __init__(self, *args, name: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name: str = name
        self.components = []
        for i in range(self.ncomponents()):
            comp = self.get_element(i)
            self.components.append([
                comp.A,
                comp.Z,
                comp.stn
            ])

    def __reduce__(self):
        return (
            Material._reconstruct,
            (
                self.name,
                self.components,
                self.density(),
                self.I(),
                self.thickness()
            ),
            None
        )

    @staticmethod
    def _reconstruct(
        name: str,
        components: List,
        density: Real,
        i_potential: Real,
        thickness: Real):
        return Material(
            components,
            name=name,
            density=density,
            i_potential=i_potential,
            thickness=thickness)


# Define types for material
CATIMA_Material = NewType('CATIMA_Material', catima.Material)  # type: ignore
NC_Material = NewType('NC_Material', Material)
MaterialLike = Union[CATIMA_Material, NC_Material]


class MaterialLayers(catima.Layers): # type: ignore

    @overload
    def __init__(
        self,
        arg: Optional[List[TrackIntersection]] = None) -> None:
        ...


    @overload
    def __init__(
        self,
        arg: Optional[List[Material]] = None) -> None:
        ...


    def __init__(
            self,
            arg = None) -> None:
        super().__init__()
        self.names: List[str] = []
        if arg:
            if all(isinstance(x, TrackIntersection) for x in arg):
                self.add_intersections(arg)
            elif all(isinstance(x, Material) for x in arg):
                self.add_materials(arg)
            else:
                raise RuntimeError('arg should be list of TrackIntersection or Material')


    def add(self, material: MaterialLike, name: Optional[str] = None) -> None:
        if type(material) is Material:
            super().add(material)
            if name:
                self.names.append(name)
            else:
                self.names.append(material.name)
        else:
            super().add(material)
            if name:
                self.names.append(name)
            else:
                raise RuntimeError('name is required.')


    def add_intersections(self, intersections: List[TrackIntersection]) -> None:
        for x in intersections:
            name = x.object.name
            if 'material' in x.object.metadata:
                mat = x.object.metadata['material']
                thickness = x.edge.Length() # type: ignore
                mat.thickness_cm(thickness * 1e-1) # mm->cm
                self.add(mat, name=name)
            else:
                logger.info(f'ignore {x.object.name} because the object does not contain material in metadata.')


    def add_materials(self, materials: List[Material]) -> None:
        for x in materials:
            self.add(x)


    def size(self) -> int:
        return self.num()
    

    def __len__(self) -> int:
        return self.size()


    def __sizeof__(self) -> int:
        return self.size()


    @overload
    def get(self, key: str) ->  Material:
        ...


    @overload
    def get(self, key: int) -> Material:
        ...


    def get(self, key) -> Material:
        if isinstance(key, int):
            idx = key
        elif isinstance(key, str):
            if key in self.names:
                idx = self.names.index(key)
            else:
                raise KeyError(f'{key} not found')
        else:
            raise TypeError
        return Material(super().get(idx), name=self.names[idx])


    def to_list(self) -> List[Material]:
        mat_list = []
        for i in range(self.size()):
            mat_list.append(self.get(i))
        return mat_list


    def __reduce__(self):
        return (
            MaterialLayers._reconstruct,
            tuple([self.to_list()]),
            None
        )


    @staticmethod
    def _reconstruct(materials: List[Material]):
        return MaterialLayers(materials)


# Define types for layers of Materials
CATIMA_Layers = NewType('CATIMA_Layers', catima.Layers) # type: ignore
NC_Layers = NewType('NC_Layers', MaterialLayers)
LayersLike = Union[CATIMA_Layers, NC_Layers]