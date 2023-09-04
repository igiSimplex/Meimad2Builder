import boto3

class AwsEbsUtils:

    def create_ebs_and_get_volume_id(self, region):
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
        volume_id = new_volume["VolumeId"]
        print(f'Created volume ID: {volume_id}')
        ec2_client.get_waiter('volume_available').wait(VolumeIds=[volume_id])
        return volume_id


    def attach_ebs_to_ec2_instance(self):
        instance_id = "aaa"



if __name__ == '__main__':
    AwsEbsUtils().create_ebs_and_get_volume_id()