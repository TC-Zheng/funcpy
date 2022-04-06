from typing import Generic, Any, TypeVar, Callable, ParamSpec

from funcpy.monad import Monad

T = TypeVar('T')
S = TypeVar('S')
R = TypeVar('R')
Q = TypeVar('Q')
P = ParamSpec('P')

class Maybe(Generic[T], Monad[T]):
    """A value that is either a success (Just) or failure (Nothing)"""
    def __init__(self, val: T):
        self.Just = val

    @classmethod
    def pure(cls, val: T) -> 'Maybe[T]':
        return Just(val)

    def bind(self: 'Maybe[T]', kleisli: 'Callable[[T], Maybe[S]]') -> 'Maybe[S]':
        # (>>=) :: m a -> (a -> m b) -> m b
        return Nothing if self is Nothing else kleisli(self.Just)

    def __str__(self):
        return "Nothing" if self is Nothing else "Just " + str(self.Just)

    def __eq__(self, other):
        return self is other if (self is Nothing or other is Nothing) else self.Just == other.Just

    # Just for type hint purpose
    def apply(self: 'Maybe[Callable[[R], S]]', ma: 'Maybe[R]') -> 'Maybe[S]':
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        return super().apply(ma)  # type: ignore

    @classmethod
    def liftM(cls, f: Callable[[R], S], a: 'Maybe[R]') -> 'Maybe[S]':
        # fmap :: a -> b -> ma -> mb
        return super().liftM(f, a)  # type: ignore




def Just(value: T) -> Maybe[T]:
    return Maybe(value)


Nothing: Maybe[Any] = Maybe(None)
