from functools import wraps


def route(router: 'Router', index: int):
    def decorator(func):
        router.add(index, func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)

        return wrapper

    return decorator


class Router:
    commands = {}

    def add(self, index, func):
        self.commands[index] = func

    def __call__(self, _self, index, conn):
        func = self.commands[index]
        func(_self, conn)
