from datetime import datetime
import os

def decor(file_name='logger.txt', file_path=None):
    if file_path is None:
        file_place = os.path.join(os.getcwd())
    else:
        file_place = os.path.join(os.path.abspath(file_path))
    file_path = os.path.join(file_place, file_name)

    def decorator_logger(old_function):
        def new_function(*args, **kwargs):
            funk_date = datetime.now().strftime("%d %B %Y  time %H:%M:%S")
            func_name = old_function.__name__
            output_value = old_function(*args, **kwargs)
            result = (f'вызвана функция {func_name}\n' +
                    f'дата и время вызова  {funk_date}\n' +
                    f'аргументы функции {args} и {kwargs}\n' +
                    f'возвращаемое значение функции {func_name}  {output_value}\n')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(result)
            return output_value
        return new_function
    return decorator_logger
