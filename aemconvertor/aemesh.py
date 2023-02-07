from typing import List, TextIO
from tqdm import tqdm

from .mesh import Point2D, Point3D, Face
from .aemfile import AEMFile


class AEMesh:
    """Represents a decoded .AEM file.
    """
    def __init__(self, vertices: List[Point3D], uvCoordinates: List[Point2D], normals: List[Point3D], faces: List[Face]):
        self.vertices = vertices
        self.uvCoordinates = uvCoordinates
        self.normals = normals
        self.faces = faces


    @classmethod
    def fromFile(cls, f: AEMFile, useTqdm: bool = True) -> "AEMesh":
        """Decode a .AEM file.
        """
        withTqdm = lambda x: tqdm(x) if useTqdm else x

        vertices =  [i for i in withTqdm(f.iterVertices())]
        uvs =       [i for i in withTqdm(f.iterUvs())]
        normals =   [i for i in withTqdm(f.iterNormals())]
        faces =     [i for i in withTqdm(f.iterFaces())]

        return cls(vertices, uvs, normals, faces)


    def writeObj(self, f: TextIO, useTqdm: bool = True):
        """Convert this mesh to WaveFront Obj format, and write to the given file.
        """
        numVertices = len(self.vertices)
        numFaces = len(self.faces)
        withTqdm = lambda x: tqdm(x) if useTqdm else x

        f.write(f"# Vertices {numVertices}\n")
        for v in withTqdm(self.vertices):
            f.write(f"v {v.x} {v.y} {v.z}\n")

        f.write(f"\n# UVs {numVertices}\n")
        for uv in withTqdm(self.uvCoordinates):
            f.write(f"vt {uv.x} {uv.y}\n")

        f.write(f"\n# Normals {numVertices}\n")
        for n in withTqdm(self.normals):
            f.write(f"vn {n.x} {n.y} {n.z}\n")

        f.write(f"\n# Faces {numFaces}\n")
        for face in withTqdm(self.faces):
            faceStr = " ".join(
                f"{i.vertexIndex}/{i.uvIndex or ''}/{i.normalIndex}"
                for i in face.indices
            )
            if faceStr:
                f.write(f"f {faceStr}\n")
