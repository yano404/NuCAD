from typing import Dict, List
import cadquery as cq


def get_components(assembly: cq.Assembly) -> Dict[str, cq.Assembly]:
        results = {}
        for x in assembly.children:
            if x.children:
                results.update(get_components(x))
            else:
                results[x.name] = x
        return results

