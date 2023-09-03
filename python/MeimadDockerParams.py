class MeimadDockerParams:
    def __init__(self, dest_root_dir):
        self.dest_docker_pack_root_dir = f"{dest_root_dir}/python_code"

    @property
    def src_docker_compose_file(self):
        return "../docker-compose.yml"

    @property
    def src_env_file(self):
        return "../.env";

    @property
    def dest_images_pack_root_dir(self):
        return f'{self.dest_docker_pack_root_dir}/images'

    @property
    def unpack_images_pack_root_dir(self):
        return "./images"

    @property
    def dest_docker_compose_dir(self):
        return f'{self.dest_docker_pack_root_dir}/docker-compose'

    @property
    def unpack_docker_compose_dir(self):
        return f'./docker-compose'

    @property
    def dest_docker_compose_file_name(self):
        return f'{self.dest_docker_compose_dir}/docker-compose.yml'

    @property
    def dest_env_file_name(self):
        return f'{self.dest_docker_compose_dir}/.env'

    @property
    def dest_images_tar_file_name(self):
        return f"{self.dest_images_pack_root_dir}/my-meimad-docker-images.tar"

    @property
    def dest_python_code_dir(self):
        return f"{self.dest_docker_pack_root_dir}"
