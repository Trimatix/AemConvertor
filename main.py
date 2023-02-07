import os
from typing import BinaryIO, Tuple
from tqdm import tqdm
import struct
from numpy import float32

def readShort(f: BinaryIO) -> int:
    return struct.unpack("h", f.read(2))[0]

def readFloat(f: BinaryIO) -> float:
    return struct.unpack("f", f.read(4))[0]

def readFloats(f: BinaryIO, num: int) -> Tuple[float, ...]:
    return tuple(struct.unpack("f", f.read(4))[0] for _ in range(num))

if __name__ == '__main__':
    option = int(input("Please choose the feature ( 1.aem2obj | 2.obj2aem ): "))
    # option = 1
    while option == 1:
        file_in = input("Please input the path of the file to be converted(Press Enter to exit):")
        file_out = file_in.replace(".aem", ".obj")
        if not file_in:
            break
        if os.path.exists(file_out):
            print(f'Warning: {file_out} already exists and will be covered! Press Enter to continue.')
            input()
            os.remove(file_out)
        file_aem = open(file_in, 'rb')
        file_obj = open(file_out, 'a')
        file_aem.seek(24)
        v_num = readShort(file_aem)
        s = f'# Vertices {v_num}\n'
        file_obj.write(s)
        print(s)
        file_aem.seek(v_num * 2 + 2, 1)
        v_x = []
        v_y = []
        v_z = []
        i = 0
        for i in tqdm(range(v_num)):
            v_x.append(readFloat(file_aem))
            v_y.append(readFloat(file_aem))
            v_z.append(readFloat(file_aem))
            s = f'v  {v_x[i]} {v_y[i]} {v_z[i]}\n'
            file_obj.write(s)
        s = f'\n# UVs {v_num}\n'
        file_obj.write(s)
        print(s)
        vt_x = []
        vt_y = []
        i = 0
        for i in tqdm(range(v_num)):
            vt_x.append(readFloat(file_aem))
            vt_y.append(readFloat(file_aem))
            s = f'vt  {vt_x[i]} {vt_y[i]}\n'
            file_obj.write(s)
        s = f'\n# Normals {v_num}\n'
        file_obj.write(s)
        print(s)
        vn_x = []
        vn_y = []
        vn_z = []
        for i in tqdm(range(v_num)):
            vn_x.append(readFloat(file_aem))
            vn_y.append(readFloat(file_aem))
            vn_z.append(readFloat(file_aem))
            s = f'vn  {vn_x[i]} {vn_y[i]} {vn_z[i]}\n'
            file_obj.write(s)
        s = f'\n# Faces {v_num // 3}\n'
        file_obj.write(s)
        print(s)
        for i in tqdm(range(v_num // 3)):
            file_obj.write('f  ')
            s = f'{i * 3 + 1}/{i * 3 + 1}/{i * 3 + 1}'
            file_obj.write(s)
            file_obj.write(' ')
            s = f'{i * 3 + 2}/{i * 3 + 2}/{i * 3 + 2}'
            file_obj.write(s)
            file_obj.write(' ')
            s = f'{i * 3 + 3}/{i * 3 + 3}/{i * 3 + 3}'
            file_obj.write(s)
            file_obj.write('\n')
        file_aem.close()
        file_obj.close()
        print('\nDone')
    if option == 2:
        print('Obj2aem is not supported yet, please wait...')
        input()
