import socket

from IgiOsUtils import *
from MeimadDockerParams import *
from MeimadPackArgsParser import PROFILE_NAME__UBUNTU_LOCAL_DEV


class MeimadEnvUtils:
    def get_src_env_file_name(self, meimadDockerParams, profile):
        src_env_file = f'{os.getcwd()}/{meimadDockerParams.src_env_file}'
        if profile is not None:
            src_env_file = src_env_file + "." + profile
        return src_env_file

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def createEnvFileForLocalMachine(self, meimadDockerParams):
        srcFileName = self.get_src_env_file_name(meimadDockerParams, None)
        destFileName = f'{os.getcwd()}/for_prod/.env.with-local-ip'
        srcString = 'host.docker.internal'
        destString = self.get_ip_address()

        print('creating an env file with local machine IP')
        print(f'copying {srcFileName} to {destFileName} ...')
        print(f"replacing '{srcString}' with '{destString}' ...")

        with open(srcFileName, 'r') as file:
            content = file.read()

        replaced_content = content.replace(srcString, destString)

        with open(destFileName, 'w') as file:
            file.write(replaced_content)
            file.close()

        print("Done!")

        return destFileName

    def copyEnvFile(self, meimad_docker_params, profile):
        if profile == PROFILE_NAME__UBUNTU_LOCAL_DEV:
            src_env_file = self.createEnvFileForLocalMachine(meimad_docker_params)
        else:
            src_env_file = self.get_src_env_file_name(meimad_docker_params, profile)

        dest_env_file = meimad_docker_params.dest_env_file_name

        if not os.path.isfile(src_env_file):
            raise Exception(f'src env file {src_env_file} does not exist !')
        else:
            print(f'{src_env_file} exists')

        IgiOsUtils().copy_file(src_env_file, dest_env_file)


if __name__ == '__main__':
    MeimadEnvUtils().createEnvFileForLocalMachine(MeimadDockerParams('.'))
