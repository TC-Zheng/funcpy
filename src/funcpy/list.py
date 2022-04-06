from typing import Generic, TypeVar, Callable, ParamSpec
from functools import reduce

from funcpy.monad import Monad

T = TypeVar('T')
S = TypeVar('S')
R = TypeVar('R')


class List(Generic[T], Monad[T]):
    def __init__(self, xs: list[T]):
        self.xs = xs

    @classmethod
    def pure(cls, val: T) -> 'List[T]':
        return List([val])

    def bind(self: 'List[T]', kleisli: 'Callable[[T], List[S]]') -> 'List[S]':
        temp = list(map(lambda x: kleisli(x).xs, self.xs))  # Apply the function to each element
        return List(reduce(lambda xs, ys: xs + ys, temp, []))  # concatenate the result

    def __iter__(self):
        return iter(self.xs)

    def __len__(self):
        return len(self.xs)

    def __str__(self):
        return "List " + str(self.xs)

    def __eq__(self, other):
        return self.xs == other.xs if type(other) is List else self.xs == other

    # Just for type hint purpose
    def apply(self: 'List[Callable[[R], S]]', ma: 'List[R]') -> 'List[S]':
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        return super().apply(ma)  # type: ignore

    @classmethod
    def liftM(cls, f: Callable[[R], S], a: 'List[R]') -> 'List[S]':
        # fmap :: a -> b -> ma -> mb
        return super().liftM(f, a)  # type: ignore
