import boto3


def get_file_count(bucket_name):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        file_count = len(response['Contents'])
        print(f'number of files {file_count}')
    else:
        print("No objects found")



if __name__ == '__main__':
    BUCKET_NAME = "my-buck_buck-1"
    get_file_count(BUCKET_NAME)