import docker


class MeimadDockerUtils:

    def delete_all_images(self, dockerClient):
        # List all Docker images
        images = dockerClient.images.list()

        # Delete each image
        for image in images:
            try:
                dockerClient.images.remove(image.id, force=True)
                print(f"Deleted image: {image.tags[0]}")
            except docker.errors.APIError as e:
                print(f"Error deleting image: {image.tags[0]} - {str(e)}")

    def execute_system_prune(self, dockerClient):
        # Run docker system prune
        prune_results = dockerClient.system.prune()

        # Print the results
        if 'SpaceReclaimed' in prune_results:
            space_reclaimed = prune_results['SpaceReclaimed']
            print(f"Space reclaimed: {space_reclaimed} bytes")
        else:
            print("No space reclaimed.")

    def delete_all_container(self, dockerClient):

        # Prune all containers
        prune_results = dockerClient.containers.prune()

        # Print the results
        if 'ContainersDeleted' in prune_results:
            containers_deleted = prune_results['ContainersDeleted']
            print(f"Deleted {containers_deleted} containers.")
        else:
            print("No containers deleted.")

    def do_docker_compose_down(self, os_utils):
        pass




if __name__ == '__main__':
    dockerClient = docker.from_env()
    utils = MeimadDockerUtils()
#    utils.execute_system_prune(dockerClient)
    utils.delete_all_images(dockerClient)
    utils.delete_all_container(dockerClient)
