from typing import Union, Tuple
from typing import NewType
import pycatima as catima

Real = Union[float]
Vector2 = Tuple[Real, Real]
Vector3 = Tuple[Real, Real, Real]

CATIMA_Material = NewType('CATIMA_Material', catima.Material)  # type: ignore
CATIMA_Layers = NewType('CATIMA_Layers', catima.Layers) # type: ignore
