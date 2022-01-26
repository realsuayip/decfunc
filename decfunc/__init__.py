import functools

__version__ = "1.0.0"
__all__ = ("wrapper",)


class wrapper:  # noqa
    def __new__(cls, *args, **kwargs):
        func = None

        if (len(args) == 1) and (not kwargs) and callable(args[0]):
            func = args[0]
            args = args[1:]

        self = super().__new__(cls)

        def _wrapper(f):
            @functools.wraps(f)
            def inner(*func_args, **func_kwargs):
                return self.mutate(f, *func_args, **func_kwargs)

            return inner

        if func is not None:
            self.__init__(*args, **kwargs)  # noqa
            return _wrapper(func)

        self.__wrapper__ = _wrapper
        return self

    def __call__(self, *args):
        return self.__wrapper__(*args)

    def mutate(self, wrapped, *args, **kwargs):
        raise NotImplementedError(
            "Method 'mutate' needs to be implemented for this wrapper."
        )
