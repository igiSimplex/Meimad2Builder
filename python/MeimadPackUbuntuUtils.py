from LinuxSshUtils import *


class MeimadPackUbuntuUtils:
    def check_if_is_aws_needed(self, profile):
        is_ubuntu_needed = False
        if profile is not None:
            if profile != '':
                if profile.find('aws') != -1:
                    is_ubuntu_needed = True
        return is_ubuntu_needed

    def copy_files_to_aws(self, profile, pack_short_dir_name, destZipFullFileName):
        if not self.check_if_is_aws_needed(profile):
            print(f"aws is not needed (profile name = {profile})")
            return

        print(f"aws is needed (profile name = {profile})")

        utils = LinuxSshUtils()
        # sshClient = utils.connectToMeimadUbuntuAsSshClient()
        sshClient = utils.connectToAwsAsSshClient()
        sftp = sshClient.open_sftp()

        try:
            home_ec2_user_meimad_dir = "/home/ec2-user/meimad"
            if (utils.fileExists(sftp, home_ec2_user_meimad_dir) == False):
                utils.executeCmdOnRemoteServer(sshClient, 'sudo mkdir meimad')

            utils.executeCmdOnRemoteServer(sshClient, "sudo chmod 777 meimad")


            utils.changeDir(sftp, home_ec2_user_meimad_dir)
            if utils.fileExists(sftp, 'python_code'):
                utils.rmtree(sftp, 'python_code')

            destZipShortFileName = f'{pack_short_dir_name}.zip'
            utils.executeCmdOnRemoteServer(sshClient, "pwd")

            if utils.fileExists(sftp, destZipShortFileName):
                utils.removeFile(sftp, destZipShortFileName)

            utils.scpCopyWithProgress(sshClient, destZipFullFileName, f'{home_ec2_user_meimad_dir}/{destZipShortFileName}')

            utils.executeCmdOnRemoteServer(sshClient, f'cd {home_ec2_user_meimad_dir}; unzip ./{destZipShortFileName}')
            utils.executeCmdOnRemoteServer(sshClient,
                                           f'cd {home_ec2_user_meimad_dir}; python3.9 ./python_code/MeimadUnpackProd.py')
        finally:
            sshClient.close()
            sftp.close()
