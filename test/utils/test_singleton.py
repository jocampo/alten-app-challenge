from utils.singleton import Singleton


class TestSingleton(metaclass=Singleton):
    def __init__(self, value):
        self.__field = value

    def get_field(self):
        return self.__field


def test_singleton():
    # Class should only be initialized once internally
    first_object = TestSingleton(10)
    second_object = TestSingleton(200)
    assert first_object.get_field() == second_object.get_field()
    # This is the ultimate test, they should both point towards the same object
    assert first_object is second_object
