import argparse

from _MeimadPackerConsts import *

class MeimadPackArgsParser:
    def parse_command_line_args(self):
        possible_profiles = ['', PROFILE_NAME__UBUNTU_LOCAL_DEV, PROFILE_NAME__UBUNTU_SIMPLEX_DEV, 'ubuntu-simplex-stage', 'ubuntu-simplex-prod']
        parser = argparse.ArgumentParser(description='Pack ')
        parser.add_argument('-profile', help='The profile', choices=possible_profiles)

        parser.print_usage()


        args = parser.parse_args()
        # print(args.accumulate(args.integers))
        local_profile = args.profile
        if local_profile is None:
            local_profile = ''

        if local_profile not in possible_profiles:
            parser.print_usage()
            raise Exception(f"Invalid profile {local_profile}")
        else:
            print(f"Profile: {local_profile}")

        return local_profile
