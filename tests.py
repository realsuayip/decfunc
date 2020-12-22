from unittest import TestCase

from decfunc import wrapper


class chicken(wrapper):
    def mutate(self, function, *args, **kwargs):
        return "Chicken!"


class mul(wrapper):
    factor: int

    def mutate(self, function, *args, **kwargs):
        return function() * self.factor


class gulp_mul(mul):
    factor: int = 0


class TestWrapper(TestCase):
    def test_not_implemented(self):
        class dec(wrapper):  # noqa
            pass

        with self.assertRaisesRegex(
            NotImplementedError,
            "Method 'mutate' needs to be implemented for this wrapper.",
        ):
            dec(lambda: 5)()

    def test_doc(self):
        @chicken
        def my_func():
            """My Docstring"""
            return

        @mul(factor=5)
        def other_func():
            """Other docstring"""
            return 5

        @chicken
        def another_func(*args, **kwargs):
            """Another docstring"""
            return 5

        @mul(factor=6)
        def some_oher_func(*args, **kwargs):
            """Some other docstring"""
            return 5

        self.assertEqual("My Docstring", my_func.__doc__)
        self.assertEqual("Other docstring", other_func.__doc__)
        self.assertEqual("Another docstring", another_func.__doc__)
        self.assertEqual("Some other docstring", some_oher_func.__doc__)

        my_func()
        other_func()

        self.assertEqual("My Docstring", my_func.__doc__)
        self.assertEqual("Other docstring", other_func.__doc__)
        self.assertEqual("Another docstring", another_func.__doc__)
        self.assertEqual("Some other docstring", some_oher_func.__doc__)

    def test_basic(self):
        @chicken
        def hen():
            return "Hen!"

        self.assertEqual("Chicken!", chicken(lambda: 5)())
        self.assertEqual("Chicken!", hen())

    def test_use_function_value(self):
        @mul(factor=5)
        def five():
            return 5

        self.assertEqual(25, five())

    def test_missing_keyword_argument(self):
        with self.assertRaisesRegex(
            ValueError, "Missing required keyword argument for 'mul': factor"
        ):

            mul(lambda: 5)

    def test_default_keyword_argument_value(self):
        @gulp_mul
        def five():
            return 5

        self.assertEqual(0, five())

        @gulp_mul(factor=2)
        def seven():
            return 7

        self.assertEqual(14, seven())

    def test_argument_style(self):
        @gulp_mul
        def four():
            return 4

        @gulp_mul()
        def three():
            return 3

        @gulp_mul(factor=0)
        def eight():
            return 8

        self.assertEqual(0, four())
        self.assertEqual(0, three())
        self.assertEqual(0, eight())

    def test_unexpected_argument(self):
        with self.assertRaisesRegex(
            ValueError, "Unexpected keyword argument for 'gulp_mul': hello"
        ):
            gulp_mul(hello=5)(lambda: 5)

    def test_forbidden_field_name(self):
        class forbidden(wrapper):
            mutate: int  # forbidden

        def func_one():
            return 1

        with self.assertRaisesRegex(
            ValueError, "Forbidden field name: 'mutate'"
        ):
            forbidden(func_one)

    def test_function_arguments(self):
        test_cls = self

        class tester(wrapper):
            def mutate(self, function, *args, **kwargs):
                test_cls.assertEqual(
                    [(1, 2), {"c": 5, "d": 3}], [args, kwargs]
                )
                return function(*args, **kwargs)

        @tester
        def my_func(a, b, c=10, d=3):
            self.assertEqual(1, a)
            self.assertEqual(2, b)
            self.assertEqual(5, c)
            self.assertEqual(3, d)
            return a + b + c + d

        self.assertEqual(11, my_func(1, 2, c=5, d=3))

    def test_class_decoration(self):
        class cls_dec(wrapper):
            def mutate(self, function, *args, **kwargs):
                return function(*args, **kwargs).x + 10

        @cls_dec
        class Something:
            def __init__(self, x):
                self.x = x

        self.assertEqual(15, Something(5))
