import os
import posixpath
from stat import S_ISDIR

import paramiko
from scp import SCPClient

from _MeimadPackerConsts import *


class LinuxSshUtils:
    def __init__(self):
        self.last_shown_percenatage_as_int = 0

    def connectAsSshClient(self, linuxIp, username, publicKeyFileName):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(linuxIp, username=username, key_filename=publicKeyFileName)
        return ssh

    def connectToMeimadUbuntuAsSshClient(self):
        # UBUNTU_DEV_IP = '83.229.74.11'
        UBUNTU_DEV_USER = 'root'
        PUBLIC_KEY_FILENAME = "C:/Users/user/.ssh/id_rsa.pub"
        return self.connectAsSshClient(UBUNTU_DEV_EXTERNAL_IP, UBUNTU_DEV_USER, PUBLIC_KEY_FILENAME)

    def connectToAwsAsSshClient(self):
        USER_NAME='ec2-user'
        PUBLIC_KEY_FILE_NAME="C:/temp/_igi_aws_conn/us_east_1_key_pair.pem"
        IP = '18.207.228.193'
        return self.connectAsSshClient(IP, USER_NAME, PUBLIC_KEY_FILE_NAME)

    def scpCopy(self, sftp, sourceFileName, destFileName):
        print(f"scp copying: src: {sourceFileName}, dest: {destFileName} ...")
        file_stats = os.stat(sourceFileName)
        print(f"file size = {file_stats.st_size / (1024 * 1024):,} MB")

        sftp.put(sourceFileName, destFileName)

    def progress(self, filename, size, sent):
        percentage = float(sent) / float(size) * 100
        percentageAsInt = int(percentage)
        if self.last_shown_percenatage_as_int != percentageAsInt:
            print(f"{filename}'s progress: {percentage:.2f}% ({sent:,} / {size:,})")
            self.last_shown_percenatage_as_int = percentageAsInt

    def scpCopyWithProgress(self, sshClient, srcFileName, destFileName):
        scp = SCPClient(sshClient.get_transport(), progress=self.progress)
        scp.put(srcFileName, destFileName)
        scp.close()

    def fileExists(self, sftp, fileName):
        try:
            exists = sftp.stat(fileName)
            print(f'file {fileName} exists')
            return True
        except IOError:
            print(f'file {fileName} does *not* exist')
            return False

    def changeDir(self, sftp, dir):
        print(f'changing dir to {dir}')
        sftp.chdir(dir)

    def executeCmdOnRemoteServer(self, sshClient, command):
        print(f"*** executing on remote server: '{command}' ...")
        stdin, stdout, stderr = sshClient.exec_command(command)

        for line in stdout:
            print(line.strip('\n'))

        for line in stderr:
            print(line.strip('\n'))

        print("************************\n\n\n")

    def removeFile(self, sftp, fileName):
        print(f'removing file {fileName}')
        sftp.remove(fileName)

    def rmtree(self, sftp, remotepath, level=0):
        print(f'removing dir {remotepath} ...')
        for f in sftp.listdir_attr(remotepath):
            rpath = posixpath.join(remotepath, f.filename)
            if S_ISDIR(f.st_mode):
                self.rmtree(sftp, rpath, level=(level + 1))
            else:
                rpath = posixpath.join(remotepath, f.filename)
                print('removing %s%s' % ('    ' * level, rpath))
                sftp.remove(rpath)
        print('removing %s%s' % ('    ' * level, remotepath))
        sftp.rmdir(remotepath)


    def get_client_ip(self, sshClient):
        # Execute a command and get the output
        stdin, stdout, stderr = sshClient.exec_command('echo Hello, World!')
        output = stdout.read().decode().strip()


        start_index = output.find('from') + len('from') + 1
        end_index = output.rfind('"')
        ip_address = output[start_index:end_index]

        print("Client IP address:", ip_address)

    def get_client_ip2(self, sshClient):
        client_ip2 = sshClient.get_transport().sock.getpeername()[0]
        print(f"Client ip 2: {client_ip2}")
        return client_ip2

    def get_client_ip3(self, sshClient):
        command = "sudo who am i --ips|awk '{print $5}'"
        command2 = "sudo who am i"
        stdin, stdout, stderr = sshClient.exec_command(command2)
        sshClient.close()
        stdout.flush()
        client_ip3 = stdout.read().decode().strip()
        # stdin = stdin.readlines()
        stderr = stderr.readlines()

    def get_client_ip4(self, sshClient):
        shell = sshClient.invoke_shell()

        # Send the "who am i" command
        shell.send("who am i\n")

        # Wait for the command to execute and receive the output
        outputs = []

        outputs = []
        for i in range (1, 5):
            output = shell.recv(1024).decode()
            outputs.append(output)
            print(f'{i} - {output}')

        result = outputs[3]
        print(f'result = {result}')
        #     outputs.append(shell.recv(1024).decode())
        #     outputs.append(shell.recv(1024).decode())
        #     outputs.append(shell.recv(1024).decode())
        #
        # while not output.endswith('$ '):  # Assuming the prompt ends with '$ '
        #     outputs.append(shell.recv(1024).decode())
        #     print(output)

        # Print the output
        # print(output)


        # a = 3



if __name__ == '__main__':
    linux_ssh_utils = LinuxSshUtils()

    sshClient = linux_ssh_utils.connectToAwsAsSshClient()
    print(sshClient)


    sourceFileName = "c:\\temp\\1.txt"
    destFileName = "/home/meimad/2.txt"



    # sshClient = linux_ssh_utils.connectToMeimadUbuntuAsSshClient()
    # client_ip = linux_ssh_utils.get_client_ip(sshClient)
    # client_ip2 = linux_ssh_utils.get_client_ip2(sshClient)
    client_ip3 = linux_ssh_utils.get_client_ip3(sshClient)
    # client_ip3 = linux_ssh_utils.get_client_ip3(sshClient)
    print("Client IP address:", client_ip3)



    sftp = sshClient.open_sftp()
    try:
        linux_ssh_utils.scpCopy(sftp, sourceFileName, destFileName)
        linux_ssh_utils.executeCmdOnRemoteServer(sshClient, 'ls -l')
    finally:
        sftp.close()
        sshClient.close()

    # linux_ssh_utils.scpCopy(sourceFileName, destFileName)
