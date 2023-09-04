import boto3



def create_ebs():
    AWS_REGION = "us-east-1"
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    new_volume = ec2_client.create_volume(
        AvailabilityZone=f'{AWS_REGION}c',
        Size=10,
        VolumeType='gp3',
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'hands-on-cloud-ebs-boto3'
                    }
                ]
            }
        ]
    )
    print(f'Created volume ID: {new_volume["VolumeId"]}')


def attach_ebs_to_ec2_instance():
    instance_id = "aaa"



if __name__ == '__main__':
    create_ebs()