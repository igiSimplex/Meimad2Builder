import boto3


def test_botox():
    client = boto3.resource(
        'ec2',
        region_name="us-east-1"
    )

    instance_details = client.create_instances(
        ImageId="ami-051f7e7f6c2f40dc1",
        MinCount=1,
        MaxCount=1,
        InstanceType="t1.micro"
    )

    print(f"created instance: {instance_details[0]}")

def test2():
    ec2 = boto3.client('ec2')
    response = ec2.describe_key_pairs()
    print(response)


if __name__ == '__main__':
    # test2()
    test_botox()