from typing import BinaryIO, List

from .binaryio import ByteLength, readUShort, readFloats
from .mesh import Point2D, Point3D, Face, FaceIndex

NUM_VERTICES_ADDRESS = 24
SPACER_LENGTH = ByteLength.short.value
COORDINATE_LENGTH = ByteLength.float.value

class AEMFile:
    """Represents a .AEM file on disk.
    This wraps an open reader of the file.
    """
    def __init__(self, file: BinaryIO):
        self._underlying = file
        file.seek(NUM_VERTICES_ADDRESS)
        self._vertices = readUShort(file)


    @property    
    def vertices(self):
        """The number of vertices in the model
        """
        return self._vertices

#region vertices    

    @property
    def verticesStartAddress(self):
        """The start address of the vertices block in the file
        """
        return NUM_VERTICES_ADDRESS \
            + SPACER_LENGTH \
            + (self.vertices * SPACER_LENGTH) \
            + SPACER_LENGTH
    

    def vertexAddress(self, vertexIndex: int) -> int:
        """The address of vertex `vertexIndex` in the file.
        `vertexIndex` is 0-based.
        """
        return self.verticesStartAddress + (3 * vertexIndex * COORDINATE_LENGTH)
    

    def iterVertices(self):
        """Read and iterate over all vertices in the file.
        """
        self._underlying.seek(self.verticesStartAddress)
        for current in range(self.vertices):
            if self._underlying.tell() != self.vertexAddress(current):
                raise RuntimeError("stream position was changed during vertices read")
            
            x, y, z = readFloats(self._underlying, 3)
            yield Point3D(x, y, z)


    def readAllVertices(self) -> List[Point3D]:
        """Read all vertices in the file into a list.
        """
        return list(self.iterVertices())
        
    
#endregion
#region UVs

    @property
    def uvsStartAddress(self):
        """The start address of the UVs block in the file
        """
        # Subtracting one here since vertexIndex is 0-based
        return self.vertexAddress(self.vertices - 1) \
            + (3 * COORDINATE_LENGTH)
    

    def uvAddress(self, uvIndex: int) -> int:
        """The address of UV `uvIndex` in the file.
        `uvIndex` is 0-based.
        """
        return self.uvsStartAddress + (2 * uvIndex * COORDINATE_LENGTH)
    

    def iterUvs(self):
        """Read and iterate over all UVs in the file.
        """
        self._underlying.seek(self.uvsStartAddress)
        for current in range(self.vertices):
            if self._underlying.tell() != self.uvAddress(current):
                raise RuntimeError("stream position was changed during UVs read")
            
            x, y = readFloats(self._underlying, 2)
            yield Point2D(x, y)


    def readAllUvs(self) -> List[Point2D]:
        """Read all UVs in the file into a list.
        """
        return list(self.iterUvs())

#endregion
#region normals

    @property
    def normalsStartAddress(self):
        """The start address of the normals block in the file
        """
        # Subtracting one here since vertexIndex is 0-based
        return self.uvAddress(self.vertices - 1) \
            + (2 * COORDINATE_LENGTH)
    

    def normalAddress(self, normalIndex: int) -> int:
        """The address of normal `normalIndex` in the file.
        `normalIndex` is 0-based.
        """
        return self.normalsStartAddress + (3 * normalIndex * COORDINATE_LENGTH)
    

    def iterNormals(self):
        """Read and iterate over all normals in the file.
        """
        self._underlying.seek(self.normalsStartAddress)
        for current in range(self.vertices):
            if self._underlying.tell() != self.normalAddress(current):
                raise RuntimeError("stream position was changed during normals read")
            
            x, y, z = readFloats(self._underlying, 3)
            yield Point3D(x, y, z)


    def readAllNormals(self) -> List[Point3D]:
        """Read all normals in the file into a list.
        """
        return list(self.iterNormals())

#endregion
#region faces

    def iterFaces(self):
        """Read and iterate over all faces in the file.
        """
        for current in range(self.vertices // 3):
            faceNum = current * 3
            indices = [
                FaceIndex(
                    vertexIndex=faceNum + vertexNum,
                    uvIndex=faceNum + vertexNum,
                    normalIndex=faceNum + vertexNum
                )
                for vertexNum in range(3) # Each face is a triangle, it has 3 vertices
            ]
            yield Face(indices)


    def readAllFaces(self) -> List[Face]:
        """Read all faces in the file into a list.
        """
        return list(self.iterFaces())

#endregion
