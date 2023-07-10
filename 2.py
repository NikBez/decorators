import os
from datetime import datetime


def logger_with_params(path):
    def logger(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            with open(path, 'a') as logs:
                to_log = dict(
                    date_time=datetime.utcnow(),
                    function_name=function.__name__,
                    args=''.join([str(item) for item in args]),
                    kwargs=''.join([f'{k}: {str(v)}, ' for k, v in kwargs.items()]),
                    result=result
                )
                for key, value in to_log.items():
                    string = str(key + ': ' + str(value)).strip(', ') + ';\n'
                    logs.write(string)
                logs.write('------------------------------------\n')
            return result
        return wrapper
    return logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_with_params(path)
        def hello_world():
            return 'Hello World'

        @logger_with_params(path)
        def summator(a, b=0):
            return a + b

        @logger_with_params(path)
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
