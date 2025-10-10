from typing import Dict, Literal, Union
import cadquery as cq


def get_components(assembly: cq.Assembly) -> Dict[str, cq.Assembly]:
        results = {}
        for x in assembly.children:
            if x.children:
                results.update(get_components(x))
            else:
                results[x.name] = x
        return results


def get_object(assy: cq.Assembly, coord: Literal['world', 'local'] = 'world') -> cq.Shape:
    obj = assy.obj

    if isinstance(obj, cq.Workplane):
        obj = obj.val()
    elif isinstance(obj, cq.Shape):
        pass
    else:
        raise RuntimeError(f'{assy.name} has no shape')

    if coord == 'world':
        loc = assy.loc * obj.location() # type: ignore
        while assy.parent is not None:
            assy = assy.parent
            loc = assy.loc * loc
        obj = obj.located(loc) # type: ignore

    if isinstance(obj, cq.Shape):
        return obj
    else:
        raise RuntimeError(f'returned object is not Shape')
