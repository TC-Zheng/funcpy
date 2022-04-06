from typing import Callable, TypeVar, Any, Type, Iterable
from inspect import signature
from functools import reduce

T = TypeVar('T')


# TODO mypy concatenate support
def curry(f, arg):
    """Take a function and its first argument to create a curried function"""
    try:
        return f(arg)
    except TypeError:
        return lambda *x: f(arg, *x)


# TODO Decorator version of curry
# def curry_dec(f):
#     """
#     Use when setup as decorator, you can partially apply function normally
#     """
#     sig = signature(f)
#     num_params = len(sig.parameters)
#
#     def inner(*args, **kwargs):
#         if len(args) + len(kwargs) < num_params:
#             return lambda *x, **kxs: f(*args, *x, **kwargs, **kxs)
#         else:
#             return f(*args, **kwargs)
#
#     return inner

def num_args(f: Callable[..., Any]) -> int:
    """Returns the number of arguments of a function"""
    return len(signature(f).parameters)


def filterM(monadic_filter, iterable):
    def folding_func(acc, x):
        monadic_bool = monadic_filter(x)
        t = type(monadic_bool)  # Python can only infer type at this stage
        # Initialize acc matching the type of the Monad (couldn't do this before)
        if acc is None:
            acc = t.pure([])
        # Add result to accumulator (Monadically) only if b is True
        return monadic_bool.bind(lambda b: t.liftM2(lambda vals, val: vals + [val], acc, t.pure(x)) if b else acc)

    return reduce(folding_func, iterable, None)


def mapM(kleisli, iterable):
    def folding_func(acc, x):
        monadic_result = kleisli(x)
        t = type(monadic_result)  # Python can only infer type at this stage
        # Initialize acc matching the type of the Monad (couldn't do this before)
        if acc is None:
            acc = t.pure([])
        # Append the monadic result
        return t.liftM2(lambda vals, val: vals + [val], acc, monadic_result)

    return reduce(folding_func, iterable, None)
