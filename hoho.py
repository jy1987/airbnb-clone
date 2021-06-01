class Dog:
    def __init__(self):
        print("wal wal")

    def pee(self):
        print("I will pee")


class Puppy(Dog):
    def pee(self):
        print("Go to Park")
        super().pee()


p = Puppy().pee()
