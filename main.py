import os
from tqdm import tqdm
import struct
from numpy import float32

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
        v_num = struct.unpack("h", file_aem.read(2))[0]
        s = f'# Vertices {v_num}\n'
        file_obj.write(s)
        print(s)
        file_aem.seek(v_num * 2 + 2, 1)
        v_x = []
        v_y = []
        v_z = []
        i = 0
        for i in tqdm(range(v_num)):
            v_x.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            v_y.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            v_z.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            s = f'v  {v_x[i]} {v_y[i]} {v_z[i]}\n'
            file_obj.write(s)
        s = f'\n# UVs {v_num}\n'
        file_obj.write(s)
        print(s)
        vt_x = []
        vt_y = []
        i = 0
        for i in tqdm(range(v_num)):
            vt_x.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            vt_y.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            s = f'vt  {vt_x[i]} {vt_y[i]}\n'
            file_obj.write(s)
        s = f'\n# Normals {v_num}\n'
        file_obj.write(s)
        print(s)
        vn_x = []
        vn_y = []
        vn_z = []
        for i in tqdm(range(v_num)):
            vn_x.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            vn_y.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            vn_z.append(float32(struct.unpack("f", file_aem.read(4))[0]))
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
