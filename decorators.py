import os
from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        with open('main.log', 'a', encoding='utf-8') as file:
            res = old_function(*args, **kwargs)
            function_time = datetime.now()

            name = old_function.__name__
            info = (
                f'Вызов функции {name} совершен {function_time.strftime("%Y-%b-%d %H:%M:%S")} c аргументами {args} и {kwargs} c результатом {res}\n')
            file.write(info)
        return res

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as file:
                res = old_function(*args, **kwargs)
                function_time = datetime.now()
                name = old_function.__name__
                info = (
                    f'Вызов функции {name} совершен {function_time.strftime("%Y-%b-%d %H:%M:%S")} c аргументами {args} и {kwargs} c результатом {res}\n')
                file.write(info)
                return res

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.len_list_of_lists = len(list_of_list)
        self.counter = -1

    def __iter__(self):
        self.counter += 1
        self.list_counter = 0
        return self

    def __next__(self):
        if self.list_counter == len(self.list_of_list[self.counter]):
            iter(self)
        if self.counter == self.len_list_of_lists:
            raise StopIteration
        self.list_counter += 1
        return self.list_of_list[self.counter][self.list_counter - 1]


@logger
def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
