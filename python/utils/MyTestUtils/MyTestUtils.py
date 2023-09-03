class MyTestUtils:
    def say2(self, str):
        print(str)

def say(param):
    print(param)


if __name__ == '__main__':
    say("Hello")
    MyTestUtils().say2("Baaa")