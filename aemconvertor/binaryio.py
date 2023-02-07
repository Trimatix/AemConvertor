from enum import Enum
from typing import BinaryIO, Tuple
from struct import unpack

class ByteLength(Enum):
    short = 2
    uShort = short
    float = 4


def readUShort(f: BinaryIO) -> int:
    """Read the next 2 bytes, and interpret this as an unsigned short.
    """
    return unpack("H", f.read(ByteLength.short.value))[0]


def readFloat(f: BinaryIO) -> float:
    """Read the next 4 bytes, and interpret this as a float.
    """
    return unpack("f", f.read(ByteLength.float.value))[0]


def readFloats(f: BinaryIO, num: int) -> Tuple[float, ...]:
    """Call readFloat `num` times, and return the results in a `num`-long tuple.
    """
    return tuple(readFloat(f) for _ in range(num))
