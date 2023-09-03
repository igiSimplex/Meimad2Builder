import yaml


class DockerComposeParser:
    def extract_image_names(self, compose_file_name):
        image_names = []
        with open(compose_file_name, 'r') as file:
            compose_data = yaml.safe_load(file)
            services = compose_data.get('services', {})
            for service in services.values():
                image = service.get('image')
                if image:
                    image_names.append(image)
        return image_names

    def print_image_names(self, compose_file_name):
        images = self.extract_image_names(compose_file_name)
        for image in images:
            print(image)


def main():
    # Specify the path to your Docker Compose file
    compose_file = '../docker-compose.yml'

    # Create a DockerComposeParser instance
    parser = DockerComposeParser()

    # Extract and print the image names
    parser.print_image_names(compose_file)


if __name__ == '__main__':
    main()
