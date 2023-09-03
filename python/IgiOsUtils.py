import os
import shutil


class IgiOsUtils:
    def execute_os_command(self, command):
        print(f"executing     : '{command}' ...")
        result = os.system(command)
        print(f'execute result: {result}')
        if result != 0:
            raise Exception(f"Failed to execute '{command}': result was {result}")

    def make_sure_dir_exists(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def delete_directory(self, dir):
        print(f'Deleting dir {dir}')
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            print('... deleted')
        else:
            print('not found :)')

    def copy_file(self, src, dest):
        print(f'Copying {src} to {dest} ...')
        shutil.copyfile(src, dest)
