import boto3

USER_DATA = '''#!/bin/bash
        echo 'test' > /tmp/hello
        sudo yum update
        sudo yum install docker -y
        sudo usermod -a -G docker ec2-user
        id ec2-user
    #   uid=1000(ec2-user) gid=1000(ec2-user) groups=1000(ec2-user),4(adm),10(wheel),190(systemd-journal),992(docker)        
        newgrp docker   
        sudo systemctl enable docker.service
        sudo systemctl start docker.service        
    '''


class AwsEc2Utils:
    def __init__(self):
        pass

    def create_instances__and_get_instance_id__and_ip_address(self, region, ami, key_pair_name):

        client = boto3.resource(
            'ec2',
            region_name=region
        )

        instance_details = client.create_instances(
            ImageId=ami,
            MinCount=1,
            MaxCount=1,
            InstanceType="t1.micro",
            SecurityGroupIds=["launch-wizard-1"],
            KeyName=key_pair_name,
            UserData=USER_DATA,
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'VolumeSize': 30,
                        'VolumeType': 'gp2'
                    }
                }
            ]
        )

        the_ec2_instance=instance_details[0]

        print(f"created instance: {the_ec2_instance}")

        print(f"waiting until running ...")
        the_ec2_instance.wait_until_running()

        the_ec2_instance.reload()

        public_ip = the_ec2_instance.public_ip_address

        print(f"created instance: {the_ec2_instance}, public ip: {public_ip}")
        return the_ec2_instance.id, public_ip


if __name__ == '__main__':
    aws_ec2_utils = AwsEc2Utils()
    ec2_instance_id, ipaddress = aws_ec2_utils.create_instances__and_get_instance_id__and_ip_address()
    a = 4
