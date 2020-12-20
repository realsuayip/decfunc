import functools


__version__ = "0.1.0"

__all__ = ["Wrapper"]


class Wrapper:
    def __init__(self, function):
        functools.update_wrapper(self, function)
        self.__decfunc__ = function

    def __call__(self, *args, **kwargs):
        cls_kwargs = getattr(self, "__kwargs")
        fields = getattr(self.__class__, "__annotations__", {})
        reserved = ("mutate", "as_decorator")

        for kwarg in cls_kwargs:
            if kwarg not in fields:
                raise ValueError("Unexpected keyword argument: %s" % kwarg)

        for field in fields:
            if field in reserved or field.startswith("__"):
                raise ValueError("Forbidden field name: '%s'" % field)

            if (field not in cls_kwargs) and (not hasattr(self, field)):
                raise ValueError(
                    "Missing required keyword argument: %s" % field
                )
            elif field in cls_kwargs:
                setattr(self, field, cls_kwargs[field])

        return self.mutate(self.__decfunc__, *args, **kwargs)

    def mutate(self, function, *args, **kwargs):
        raise NotImplementedError(
            "Method 'mutate' needs to be implemented for this class."
        )

    @classmethod
    def as_decorator(cls):
        def outer(initial=None, **kwargs):
            def decorator(func):
                wrapped = cls(func)
                setattr(wrapped, "__kwargs", kwargs)
                return wrapped

            return decorator(initial) if initial else decorator

        return outer
