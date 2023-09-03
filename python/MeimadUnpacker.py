import sys

from MeimadDockerParams import *
from IgiDockerComposeUtils import *
from IgiOsUtils import *


class MeimadUnpacker:

    def unpack(self, rootDir):
        # print(sys.argv[1])
        # rootDir = "d:\\temp\\1"
        # rootDir = '.' # d:/temp/1/meimad-docker-compose-pack2'
        # if len(sys.argv) > 1:
        #     rootDir = sys.argv[0]

        # rootDir = "."
        meimad_docker_params = MeimadDockerParams(rootDir)
        docker_compose_file_name = meimad_docker_params.dest_docker_compose_file_name
        images_tar_file_name = meimad_docker_params.dest_images_tar_file_name

        igi_docker_compose_utils = IgiDockerComposeUtils(IgiOsUtils())
        igi_docker_compose_utils.unpack_docker_images(images_tar_file_name)
        igi_docker_compose_utils.docker_compose_down(meimad_docker_params.dest_docker_compose_file_name)
        igi_docker_compose_utils.docker_compose_up_no_build(meimad_docker_params.dest_docker_compose_file_name)
