from DockerComposeParser import *
from IgiDockerComposeUtils import *
from MeimadEnvUtils import *
from MeimadPackArgsParser import MeimadPackArgsParser
from MeimadPackUbuntuUtils import *
from ZipUtils import *

docker_compose_utils = IgiDockerComposeUtils(IgiOsUtils())


def copy_python_code_files():
    dest_python_code_dir = meimad_docker_params.dest_python_code_dir
    if not os.path.exists(dest_python_code_dir):
        os.makedirs(dest_python_code_dir)
    cwd = os.getcwd().replace("\\", "/")
    IgiOsUtils().execute_os_command(f'COPY "{cwd}/*.py" "{dest_python_code_dir}"')


def copy_docker_compose_yml_and_env():
    if not os.path.exists(meimad_docker_params.dest_docker_compose_dir):
        os.makedirs(meimad_docker_params.dest_docker_compose_dir)

    src_compose_file = f'{os.getcwd()}/{meimad_docker_params.src_docker_compose_file}'
    dest_compose_file = meimad_docker_params.dest_docker_compose_file_name
    IgiOsUtils().execute_os_command(f'copy "{src_compose_file}" "{dest_compose_file}"')

    meimad_env_utils.copyEnvFile(meimad_docker_params, profile)


def delete_old_pack_dir(to_ask_permission):
    pack_root_dir = meimad_docker_params.dest_docker_pack_root_dir
    if os.path.isdir(pack_root_dir):
        if to_ask_permission:
            confirmation = input(f'Are you sure you want to delete the directory {pack_root_dir}?')
        else:
            confirmation = "y"

        if confirmation.lower() == "y":
            try:
                # os.rmdir(pack_root_dir)
                shutil.rmtree(pack_root_dir)
                print(f'directory {pack_root_dir} has been deleted')
            except OSError as e:
                raise Exception(f"Failed to delete directory {pack_root_dir}: {e}")
        else:
            raise Exception(f"Failed to delete directory {pack_root_dir} (the user chose not to delete it)")


def delete_old_images__and__delete_old_pack_dir():
    docker_compose_utils.docker_compose_down(src_docker_compose_file_name)
    for image_name in all_image_names:
        docker_compose_utils.remove_docker_image(image_name)
    delete_old_pack_dir(False)


def build_new_images(to_use_cache):
    docker_compose_utils.docker_compose_build(meimad_docker_params.src_docker_compose_file, to_use_cache)


def pack_images_tar_file():
    if not os.path.exists(meimad_docker_params.dest_images_pack_root_dir):
        os.makedirs(meimad_docker_params.dest_images_pack_root_dir)
    docker_compose_utils.pack_docker_images(all_image_names, dest_images_tar_file_name)


def do_zip(destZipFileName):
    initialDir = os.getcwd()
    os.chdir(dest_dir_full_name)

    ZipUtils().zipDir(destZipFileName, ".")

    os.chdir(initialDir)


if __name__ == '__main__':
    profile = MeimadPackArgsParser().parse_command_line_args()
    # profile = PROFILE_NAME__UBUNTU_LOCAL_DEV
    # profile = None
    # profile = PROFILE_NAME__UBUNTU_SIMPLEX_DEV
    profile = PROFILE_NAME__AWS
    print(f'using profile {profile}')

    dest_dir_parent = "d:/temp/1"
    pack_short_dir_name = "meimad-docker-compose-pack2"
    dest_dir_full_name = f'{dest_dir_parent}/{pack_short_dir_name}'
    meimad_docker_params = MeimadDockerParams(dest_dir_full_name)

    meimad_env_utils = MeimadEnvUtils()
    print(f'using env file {meimad_env_utils.get_src_env_file_name(meimad_docker_params, profile)}')

    IgiOsUtils().delete_directory(dest_dir_parent)
    src_docker_compose_file_name = meimad_docker_params.src_docker_compose_file  # "../docker-compose.yml"
    dest_images_tar_file_name = meimad_docker_params.dest_images_tar_file_name  # "d:/temp/my-meimad-dockers.tar"
    dest_docker_compose_file_name = meimad_docker_params.dest_docker_compose_file_name

    all_image_names = DockerComposeParser().extract_image_names(src_docker_compose_file_name)


    delete_old_images__and__delete_old_pack_dir()

    to_use_cache = True  # for performance
    build_new_images(to_use_cache)

    pack_images_tar_file()

    copy_python_code_files()
    copy_docker_compose_yml_and_env()

    destZipFullFileName = f'{dest_dir_full_name}.zip'
    do_zip(destZipFullFileName)

    MeimadPackUbuntuUtils().copy_files_to_aws(profile, pack_short_dir_name, destZipFullFileName)
