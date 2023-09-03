from LinuxSshUtils import *


class MeimadPackUbuntuUtils:
    def check_if_is_ubuntu_needed(self, profile):
        is_ubuntu_needed = False
        if profile is not None:
            if profile != '':
                if profile.find('ubuntu') != -1:
                    is_ubuntu_needed = True
        return is_ubuntu_needed

    def copy_files_to_ubuntu(self, profile, pack_short_dir_name, destZipFullFileName):
        if not self.check_if_is_ubuntu_needed(profile):
            print(f"ubuntu is not needed (profile name = {profile})")
            return

        print(f"ubuntu is needed (profile name = {profile})")

        utils = LinuxSshUtils()
        sshClient = utils.connectToMeimadUbuntuAsSshClient()
        sftp = sshClient.open_sftp()

        try:
            home_meimad_dir = "/home/meimad"
            utils.changeDir(sftp, home_meimad_dir)
            if utils.fileExists(sftp, 'python_code'):
                utils.rmtree(sftp, 'python_code')

            destZipShortFileName = f'{pack_short_dir_name}.zip'
            utils.executeCmdOnRemoteServer(sshClient, "pwd")

            if utils.fileExists(sftp, destZipShortFileName):
                utils.removeFile(sftp, destZipShortFileName)

            utils.scpCopyWithProgress(sshClient, destZipFullFileName, f'{home_meimad_dir}/{destZipShortFileName}')

            utils.executeCmdOnRemoteServer(sshClient, f'cd {home_meimad_dir}; unzip ./{destZipShortFileName}')
            utils.executeCmdOnRemoteServer(sshClient,
                                           f'cd {home_meimad_dir}; python3.10 ./python_code/MeimadUnpackProd.py')
        finally:
            sshClient.close()
            sftp.close()
