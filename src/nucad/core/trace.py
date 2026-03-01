from dataclasses import dataclass
from typing import Any, List, Literal, Optional
import logging
import copy
import pycatima as catima

from nucad.types import Real
from nucad.core.particle import Particle
from nucad.core.track import Track, TrackIntersection, intersect_assembly_track
from nucad.core.material import MaterialLayers

logger = logging.getLogger(__name__)

@dataclass
class Trace:
    name: str
    intersection: TrackIntersection
    time: Real
    info: Any


class TraceContainer:
    def __init__(self, traces: Optional[List[Trace]] = None):
        self.traces = [] if traces is None else list(traces)

    def find(self, name: str) -> List[Trace]:
        return [tr for tr in self.traces if tr.name == name]
    
    def append(self, tr: Trace):
        self.traces.append(tr)


def trace_catima(
        particle: Particle,
        intersections: List[TrackIntersection]):
    p = copy.copy(particle)
    proj = catima.Projectile( # type: ignore
        p.A,
        p.Z,
        p.charge_state,
        p.kinetic_energy / p.A)
    
    container = TraceContainer()
    time = 0.0 # ns

    for x in intersections:
        info = None
        tin = time
        if x.object:
            name = x.name
            if 'material' in x.object.metadata:
                mat = x.object.metadata['material']
                thickness = x.edge.Length() # type: ignore
                mat.thickness_cm(thickness * 1e-1) # mm->cm
                info = catima.calculate(proj, mat) # type: ignore
                time += info.tof
                proj.T(info.Eout)
                p.T(info.Eout * proj.A())
            else:
                logger.info(f'ignore {x.name} because the object does not contain material in metadata.')
                thickness = x.edge.Length() # type: ignore
                time += p.tof(thickness)
        else:
            name = x.name
            thickness = x.edge.Length() # type: ignore
            time += p.tof(thickness)
        
        container.append(Trace(
            name = name,
            intersection = x,
            time = tin,
            info = info
        ))
    
    return container
    
def trace(
        particle: Particle,
        intersections: List[TrackIntersection],
        engine: Literal['catima'] = 'catima'
    ) -> TraceContainer | None:
    if engine == 'catima' :
        return trace_catima(particle, intersections)
    else:
        return None


