from IgiOsUtils import *


class IgiDockerComposeUtils:
    def __init__(self, igi_os_utils: IgiOsUtils):
        self.igi_os_utils = igi_os_utils

    def execute_os_command(self, command):
        self.igi_os_utils.execute_os_command(command)

    def docker_compose_down(self, docker_compose_file_name):
        self.igi_os_utils.execute_os_command(f'docker-compose -f {docker_compose_file_name} down')

    def docker_compose_build(self, docker_compose_file_name, to_use_cache):
        use_cache_string = ""
        if not to_use_cache:
            use_cache_string = "--no-cache"

        self.igi_os_utils.execute_os_command(f'docker-compose -f {docker_compose_file_name} build {use_cache_string}')

    def docker_compose_up(self, docker_compose_file_name):
        self.igi_os_utils.execute_os_command(f'docker-compose -f {docker_compose_file_name} up')

    def docker_compose_up_no_build(self, docker_compose_file_name):
        self.igi_os_utils.execute_os_command(f'docker-compose -f {docker_compose_file_name} up --no-build')

    def remove_docker_image(self, docker_image):
        self.igi_os_utils.execute_os_command(f'docker image rm -f {docker_image}')

    def pack_docker_images(self, docker_image_names, target_tar_file_name):
        image_names_as_string = " ".join(docker_image_names)
        command = f"docker save -o {target_tar_file_name} {image_names_as_string}"
        self.execute_os_command(command)

    def unpack_docker_images(self, docker_tar_file_name):
        self.execute_os_command(f'docker load < {docker_tar_file_name}')
