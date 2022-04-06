from abc import abstractmethod
from typing import Generic, TypeVar

from funcpy.functions import curry, num_args

T = TypeVar('T')
S = TypeVar('S')

class Monad(Generic[T]):
    # Methods that needs to be implemented
    @classmethod
    @abstractmethod
    def pure(cls, value):
        """Put the value into minimal context of the monad"""
        ...

    @abstractmethod
    def bind(self, kleisli):
        """Pass a monadic value to a function that take normal value and output monadic value"""
        ...

    # Methods that you get for free as a monad
    def apply(self, ma):
        """Apply a normal function inside a monad to monadic value"""
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        # Implementation in terms of bind (Haskell syntax
        # f ap v = do
        #   f' <- f
        #   v' <- v
        #   return $ f' v'
        return self.bind(
            lambda f: ma.bind(
                lambda a:
                    type(ma).pure(curry(f, a))))

    @classmethod
    def liftM(cls, f, a):
        """Lifts a normal function f: a -> b to monadic function f': m a -> m b"""
        # fmap :: a -> b -> ma -> mb
        return cls.pure(f).apply(a)

    @classmethod
    def liftM2(cls, f, a, b):
        # liftM2 :: ((a -> b) -> c) -> ((m a -> m b) -> m c)
        return cls.pure(f).apply(a).apply(b)

    @classmethod
    def liftM3(cls, f, a, b, c):
        return cls.pure(f).apply(a).apply(b).apply(c)

    @classmethod
    def liftM4(cls, f, a, b, c, d):
        return cls.pure(f).apply(a).apply(b).apply(c).apply(d)

    @classmethod
    def liftM5(cls, f, a, b, c, d, e):
        return cls.pure(f).apply(a).apply(b).apply(c).apply(d).apply(e)
