from unittest import TestCase

from decfunc import Wrapper


class TestWrapper(TestCase):
    def setUp(self):
        class Chicken(Wrapper):
            def mutate(self, function, *args, **kwargs):
                return "Chicken!"

        class Mul(Wrapper):
            factor: int

            def mutate(self, function, *args, **kwargs):
                return function() * self.factor

        class GulpMul(Mul):
            factor: int = 0

        self.chicken = Chicken.as_decorator()
        self.mul = Mul.as_decorator()
        self.gulp_mul = GulpMul.as_decorator()

    def test_not_implemented(self):
        class MyWrapper(Wrapper):
            pass

        dec = MyWrapper.as_decorator()

        with self.assertRaisesRegex(
            NotImplementedError,
            "Method 'mutate' needs to be implemented for this class.",
        ):
            dec(lambda: 5)()

    def test_doc(self):
        @self.chicken
        def my_func():
            """My Docstring"""
            return

        self.assertEqual("My Docstring", my_func.__doc__)

    def test_basic(self):
        @self.chicken
        def hen():
            return "Hen!"

        self.assertEqual("Chicken!", self.chicken(lambda: 5)())
        self.assertEqual("Chicken!", hen())

    def test_use_function_value(self):
        @self.mul(factor=5)
        def five():
            return 5

        self.assertEqual(25, five())

    def test_missing_keyword_argument(self):
        @self.mul
        def five():
            return 5

        with self.assertRaisesRegex(
            ValueError, "Missing required keyword argument: factor"
        ):
            five()

    def test_default_keyword_argument_value(self):
        @self.gulp_mul
        def five():
            return 5

        self.assertEqual(0, five())

        @self.gulp_mul(factor=2)
        def seven():
            return 7

        self.assertEqual(14, seven())

    def test_argument_style(self):
        @self.gulp_mul
        def four():
            return 4

        @self.gulp_mul()
        def three():
            return 3

        @self.gulp_mul(factor=0)
        def eight():
            return 8

        self.assertEqual(0, four())
        self.assertEqual(0, three())
        self.assertEqual(0, eight())

    def test_unexpected_argument(self):
        @self.gulp_mul(hello=5)
        def five():
            return 5

        with self.assertRaisesRegex(
            ValueError, "Unexpected keyword argument: hello"
        ):
            five()

    def test_forbidden_field_name(self):
        class ForbiddenOne(Wrapper):
            mutate: int  # forbidden

        one = ForbiddenOne.as_decorator()

        @one
        def func_one():
            return 1

        with self.assertRaisesRegex(
            ValueError, "Forbidden field name: 'mutate'"
        ):
            func_one()

    def test_function_arguments(self):
        test_cls = self

        class Tester(Wrapper):
            def mutate(self, function, *args, **kwargs):
                test_cls.assertEqual(
                    [(1, 2), {"c": 5, "d": 3}], [args, kwargs]
                )
                return function(*args, **kwargs)

        @Tester.as_decorator()
        def my_func(a, b, c=5, d=3):
            return a + b + c + d

        self.assertEqual(11, my_func(1, 2, c=5, d=3))

    def test_class_decoration(self):
        class ClassWrapper(Wrapper):
            def mutate(self, function, *args, **kwargs):
                return function(*args, **kwargs).x + 10

        @ClassWrapper.as_decorator()
        class Something:
            def __init__(self, x):
                self.x = x

        self.assertEqual(15, Something(5))
