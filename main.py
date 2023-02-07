import os

from aemconvertor.aemesh import AEMesh
from aemconvertor.aemfile import AEMFile
    

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

        with open(file_in, 'rb') as file_aem:
            aemfile = AEMFile(file_aem)
            mesh = AEMesh.fromFile(aemfile)
            with open(file_out, 'a') as file_obj:
                mesh.writeObj(file_obj)

        print('\nDone')
    if option == 2:
        print('Obj2aem is not supported yet, please wait...')
        input()
