import boto3

from AwsEc2Utils import AwsEc2Utils
from AwsEbsUtils import AwsEbsUtils

US_EAST_1_AMI = "ami-051f7e7f6c2f40dc1"
US_EAST_1_REGION_NAME = "us-east-1"
US_EAST_1_KEY_PAIR = "us_east_1_key_pair"

TEL_AVIV_AMI = "ami-0e2abb0d8da8f161a"
TEL_AVIV_REGION_NAME = "il-central-1"
TEL_AVIV_KEY_PAIR = "igi-meimad2-test"

class AwsUtils:
    def attach_ebs_volume_id_to_ec2_instance(self, ebs_volume_id, ec2_instance_id):
        ec2 = boto3.client('ec2')
        response = ec2.attach_volume(
            Device='/dev/xvdf',
            InstanceId=ec2_instance_id,
            VolumeId=ebs_volume_id
        )
        print(f"attach response: {response}")



if __name__ == '__main__':
    aws_ec2_utils = AwsEc2Utils()
    # ebs_volume_id = AwsEbsUtils().create_ebs_and_get_volume_id(REGION_NAME_US_EAST_1)
    ec2_instance_id, ip_address = aws_ec2_utils.create_instances__and_get_instance_id__and_ip_address(US_EAST_1_REGION_NAME, US_EAST_1_AMI, US_EAST_1_KEY_PAIR)

    # AwsUtils().attach_ebs_volume_id_to_ec2_instance(ebs_volume_id, ec2_instance_id)

    a = 9