import functools


__version__ = "0.2.1"

__all__ = ("wrapper",)


class wrapper:
    __reserved_fields = ("mutate",)

    def __init__(self, func=None, **options):
        self.options = options
        self.__decfunc__ = func

        if func is not None:
            self.__set_fields()
            functools.update_wrapper(self, self.__decfunc__)

    def __call__(self, *func_args, **func_kwargs):
        if self.__decfunc__ is not None:
            return self.mutate(self.__decfunc__, *func_args, **func_kwargs)

        func = func_args[0]
        return self.__class__(func, **self.options)

    def __str__(self):
        return self.__class__.__name__

    def __set_fields(self):
        fields = getattr(self.__class__, "__annotations__", {})

        for option in self.options:
            if option not in fields:
                raise ValueError(
                    "Unexpected keyword argument for '%s': %s" % (self, option)
                )

        for field in fields:
            if field in self.__reserved_fields or field.startswith("__"):
                raise ValueError("Forbidden field name: '%s'" % field)

            if (field not in self.options) and (not hasattr(self, field)):
                raise ValueError(
                    "Missing required keyword argument for '%s': %s"
                    % (self, field)
                )
            elif field in self.options:
                setattr(self, field, self.options[field])

    def mutate(self, wrapped, *args, **kwargs):
        raise NotImplementedError(
            "Method 'mutate' needs to be implemented for this wrapper."
        )
