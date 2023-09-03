import os
import zipfile


class ZipUtils:
    def zipDirInternal(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                full_file_name = os.path.join(root, file)
                print(f' zipping {full_file_name} ...')
                ziph.write(full_file_name)

    def zipDir(self, destFileName, dirNameToPack):
        print(f'zipping directory {dirNameToPack} to {destFileName} ...')
        zipf = zipfile.ZipFile(destFileName, 'w', zipfile.ZIP_DEFLATED)
        self.zipDirInternal(dirNameToPack, zipf)
        zipf.close()
        print('zipping done !')


if __name__ == '__main__':
    pathToPack = "d:\\temp\\1"
    destZipFileName = f'{pathToPack}.zip'
    ZipUtils().zipDir(destZipFileName, pathToPack)
