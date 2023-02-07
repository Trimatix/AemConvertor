from typing import List, Optional


class Point2D:
    """A 2-tuple of coordinates.
    """
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y


class Point3D:
    """A 3-tuple of coordinates.
    """
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z


class FaceIndex:
    """An entry in a WaveFront Obj Face.
    Consists of indices for a vertex, an optional uv, and a normal.
    """
    def __init__(self, vertexIndex: int, uvIndex: Optional[int], normalIndex: int) -> None:
        self.vertexIndex = vertexIndex
        self.uvIndex = uvIndex
        self.normalIndex = normalIndex


class Face:
    """A WaveFront Obj Face.
    Consists of a list of references to vertices, normals, and optionally UVs, declared elsewhere in the file.
    """
    def __init__(self, indices: List[FaceIndex]) -> None:
        self.indices = indices
        