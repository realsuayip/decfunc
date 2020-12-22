## decfunc

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Creating decorators with arguments made easy.

Creating decorators in Python is easy, unless you want to use
arguments. The aim of this library to abstract away some code
that makes argument-ed decorators work. 

## Documentation

This library only contains one class: `wrapper`. The `mutate`
method of this class is responsible for your business logic.
You can simply use a class inheriting from `wrapper` as the
decorator.  For example:

````python
from decfunc import wrapper


class square_root(wrapper):
    def mutate(self, wrapped, *args, **kwargs):
        return wrapped(*args, **kwargs) ** (1 / 2)


@square_root
def get_number(*args, **kwargs):
    return 4


get_number()  # 2.0
````

In this example, decorated function's return value is mutated so
that its square root is returned instead. As you can see
`mutate` method takes a `wrapped`, which is the decorated
class or function, and `*args`, `**kwargs`, which correspond
to given args and kwargs of the decorated function/class.

Now lets change this a little bit so that we can give pass
an argument named `n`, which will denote to nth root, instead
of square root.

````python
from decfunc import wrapper


class nth_root(wrapper):
    n: int = 2

    def mutate(self, wrapped, *args, **kwargs):
        return wrapped(*args, **kwargs) ** (1 / self.n)


@nth_root(n=3)
def get_number(*args, **kwargs):
    return 27


@nth_root
def get_another_number(*args, **kwargs):
    return 16


get_number()  # 3.0
get_another_number()  # 4.0
````

As you can see, in order to add arguments to the decorator
you need to use annotation syntax. If you assign a value to
the argument, it will be used as default argument;
calling bare `@nth_root` behaves just like `@square_root`.
Refrain from using mutable objects as default values.

And that's about it! If you don't specify a default value,
a `ValueError` will be raised indicating that the field is required.
