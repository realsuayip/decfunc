import functools
from inspect import signature

__version__ = "1.0.0"

__all__ = ("wrapper",)


class wrapper:  # noqa
    def __new__(cls, *args, **kwargs):
        func = None

        if args and callable(args[0]):
            func = args[0]
            args = args[1:]

        self = super().__new__(cls)
        signature(self.__init__).bind(*args, **kwargs)

        def _wrapper(f):
            @functools.wraps(f)
            def inner(*func_args, **func_kwargs):
                signature(f).bind(*func_args, **func_kwargs)
                self.__init__(*args, **kwargs)  # noqa
                return self.mutate(f, *func_args, **func_kwargs)

            return inner

        self.__wrapper__ = _wrapper

        if func is not None:
            return self.__wrapper__(func)

        return self

    def __call__(self, *args):
        return self.__wrapper__(*args)

    def mutate(self, wrapped, *args, **kwargs):
        raise NotImplementedError(
            "Method 'mutate' needs to be implemented for this wrapper."
        )
