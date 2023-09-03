import argparse


def test():
    parser = argparse.ArgumentParser(description='Pack ')
    parser.add_argument('-profile', help='The profile', choices=['igal', 'dev', 'stage', 'roee'])

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    profile = args.profile
    print(f"Profile: {profile}")
    return profile


if __name__ == '__main__':
    test()
