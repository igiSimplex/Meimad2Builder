import sys


def test2():
    print(f"x1 = {x1}")
    print(f"from test2: x = {x}")


def test():
    global x1
    x1 = "my x1"
    print(f"x = {x}")
    test2()


if __name__ == '__main__':
    print(sys.argv)
    x = "my x"
    test()