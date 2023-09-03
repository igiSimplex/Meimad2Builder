from python.LinuxSshUtils import LinuxSshUtils


def install_pyton_3_10():
    pass


if __name__ == '__main__':
    utils = LinuxSshUtils()
    # sshClient = utils.connectToMeimadUbuntuAsSshClient()
    sshClient = utils.connectToAwsAsSshClient()
    sftp = sshClient.open_sftp()

    install_pyton_3_10()