import datetime
import os
import subprocess
import threading

import boto3
import s3fs as s3fs

from Meimad2Builder.python.IgiOsUtils import IgiOsUtils


def do_s3_upload():
    s3 = boto3.resource("s3")

    bucket = s3.Bucket(BUCKET_NAME)
    OBJECT_NAME = "aaaa"
    test = bucket.put_object(Key=OBJECT_NAME, Body="c:/temp/1.txt")
    bucket.upload_file('c:/temp/1.txt', 'folder/sub/path')

    # s3_client = boto3.client('s3')
    # test = s3_client.upload_file('c:/temp/1.txt', bucket)

    a = 3;


def do_s3_file_upload_recursively(local_path):
    #    local_path = local_path.replace("\\", "/")
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    uploaded_count = 0

    s3_key_prefix = ''
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file).replace("\\", "/")
            s3_object_key = os.path.join(s3_key_prefix, os.path.relpath(local_file_path, local_path)).replace("\\", '/')
            uploaded_count = uploaded_count + 1
            print(f'uploading "{local_file_path}" as "{s3_object_key}" (total uploaded: {uploaded_count})')
            result = bucket.upload_file(local_file_path, s3_object_key, ExtraArgs={'ACL': 'public-read'})
            print(f'result = {result}')


def s3fs_test():
    s3 = s3fs.S3FileSystem(anon=True)
    files = s3.ls(BUCKET_NAME)
    print(files)


def capture_stream(stream, label):
    for line in iter(stream.readline, b''):
        print(label, line, end="")


def execute_command_with_logs(command):
    print(f"Executing command with logs: '{command}'")

    process = subprocess.Popen(
        command,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    stderr_thread = threading.Thread(target=capture_stream, args=(process.stderr, "stderr:"))
    stdout_thread = threading.Thread(target=capture_stream, args=(process.stdout, "stdout:"))

    stdout_thread.start()
    stderr_thread.start()

    process.wait()

    stderr_thread.join()
    stdout_thread.join()

    if process.returncode == 0:
        print(f'command was successful {command}')
    else:
        print(f'command error (result = {process.returncode}, command = {command}')


def upload_via_aws_cli():
    start_time = datetime.datetime.now()
    src_dir = "c:/data"
    operation_desc = f"syncing {src_dir} to bucket {BUCKET_NAME}"
    print(f"{operation_desc} start time: {start_time}")

    command = f"aws s3 sync {src_dir} s3://{BUCKET_NAME} --acl public-read"

    execute_command_with_logs(command)

    # IgiOsUtils().execute_os_command()

    end_time = datetime.datetime.now()
    diff = end_time - start_time
    print(f"{operation_desc} start time: {start_time}, end_time: {end_time}, diff: {diff}")


if __name__ == '__main__':
    # do_s3_upload()
    BUCKET_NAME = 'my-buck-buck-1'
    # do_s3_file_upload_recursively("c:/temp/14")
    # do_s3_file_upload_recursively("c:/data")
    # s3fs_test()
    upload_via_aws_cli()
