import boto3

US_EAST_1_AMI = "ami-051f7e7f6c2f40dc1"
TEL_AVIV_AMI = "ami-0e2abb0d8da8f161a"
REGION_NAME_US_EAST_1 = "us-east-1"
REGION_NAME_TEL_AVIV = "il-central-1"
US_EAST_1_KEY_PAIR = "us_east_1_key_pair"
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


# def create_instances_and_get_ip_address():
#     region_name = REGION_NAME_US_EAST_1
#     ami = US_EAST_1_AMI
#
#     client = boto3.resource(
#         'ec2',
#         region_name=region_name
#     )
#
#     instance_details = client.create_instances(
#         ImageId=US_EAST_1_AMI,
#         MinCount=1,
#         MaxCount=1,
#         InstanceType="t1.micro",
#         SecurityGroupIds=["launch-wizard-1"],
#         KeyName=US_EAST_1_KEY_PAIR,
#         UserData=USER_DATA
#     )
#
#
#
#     the_instance=instance_details[0]
#
#     print(f"created instance: {the_instance}")
#
#     print(f"waiting until running ...")
#     the_instance.wait_until_running()
#
#     the_instance.reload()
#
#     public_ip = the_instance.public_ip_address
#
#     print(f"created instance: {instance_details[0]}, public ip: {public_ip}")
#     return public_ip


def test2():
    ec2 = boto3.client('ec2')
    response = ec2.describe_key_pairs()
    print(response)


def run_instance_working():
    ec2_client = boto3.client("ec2", region_name=REGION_NAME_US_EAST_1)
    instances = ec2_client.run_instances(
        ImageId=US_EAST_1_AMI,
        MinCount=1,
        MaxCount=1,
        InstanceType="t1.micro",
        SecurityGroupIds=["launch-wizard-1"],
        KeyName=US_EAST_1_KEY_PAIR,
        UserData=USER_DATA
    )
    the_instance=instances["Instances"][0]
    # the_instance.wait_until_running()
    the_instance.reload()

    public_ip = the_instance.public_ip_address

    print(f"instance: {the_instance}, public id: {public_ip}")
    print(instances["Instances"][0]["InstanceId"])


if __name__ == '__main__':
    # run_instance_working()
    create_instances_and_get_ip_address()
    #test_botox()
