## decfunc

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Creating decorators with arguments made easy.

Creating decorators in Python is easy, unless you want to use
arguments. The aim of this library to abstract away some code
that makes argument-ed decorators work. 

## Documentation

This library only contains one class: `Wrapper`. The `mutate`
method of this class is responsible for the business logic.
You can convert this class to decorator using the class method
`as_decorator`. Here is a simple example:

````python
from decfunc import Wrapper


class SquareRoot(Wrapper):
    def mutate(self, function, *args, **kwargs):
        return function(*args, **kwargs) ** (1 / 2)


square = SquareRoot.as_decorator()


@square
def get_number(*args, **kwargs):
    return 4


get_number()  # 2.0
````

In this example, decorated function's return value is mutated so
that its square root is returned instead. As you can see
`mutate` method takes a `function`, which is the decorated
class or function, and `*args`, `**kwargs`, which correspond
to given args and kwargs of the decorated function/class.

Now lets change this a little bit so that we can give pass
an argument named `n`, which will denote to nth root, instead
of square root.

````python
from decfunc import Wrapper


class NthRoot(Wrapper):
    n: int = 2

    def mutate(self, function, *args, **kwargs):
        return function(*args, **kwargs) ** (1 / self.n)


root = NthRoot.as_decorator()


@root(n=3)
def get_number(*args, **kwargs):
    return 27


@root
def get_another_number(*args, **kwargs):
    return 16


get_number()  # 3.0
get_another_number() # 4.0
````

As you can see, in order to add arguments to the decorator
you need to use annotation syntax. If you assign a value to
the argument, it will be used as default argument;
calling bare `@root` behaves just like `@square`.
Refrain from using mutable objects as default values.

And that's about it! If you don't specify a default value,
a `ValueError` will be raised indicating that the field is required.
