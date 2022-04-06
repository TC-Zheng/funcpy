from abc import abstractmethod, ABC
from typing import Generic, Any, TypeVar, Callable, Union, Type, get_args

from funcpy.monad import Monad

T = TypeVar('T')
V = TypeVar('V')
S = TypeVar('S')
R = TypeVar('R')
numeric = Union[int, float, complex]


class _Writer(Monad[V]):

    def __init__(self, value: V, log):
        self.log = log
        self.value = value

    @classmethod
    def pure(cls, value):
        return cls(value, cls._monoid_id())

    def bind(self, kleisli):
        result = kleisli(self.value)
        return self.__class__(result.value, self._monoid_operation(self.log, result.log))

    def __str__(self):
        return f"({str(self.value)}, {str(self.log)})"

    def __eq__(self, other):
        return self.value == other.value and self.log == other.log

    @staticmethod
    @abstractmethod
    def _monoid_id():
        ...

    @staticmethod
    @abstractmethod
    def _monoid_operation(a, b):
        ...

    @classmethod
    @abstractmethod
    def tell(cls, log):
        ...


class WriterStr(_Writer[V], Generic[V]):
    """Monoid: String with concatenation"""
    # Actual implementation needed
    @staticmethod
    def _monoid_id() -> str:
        return ""

    @staticmethod
    def _monoid_operation(a: str, b: str) -> str:
        return a + b

    @classmethod
    def tell(cls, log: str) -> 'WriterStr[Any]':
        return WriterStr(None, log)

    # For type hint purpose
    @classmethod
    def pure(cls, value: V) -> 'WriterStr[V]':
        return super().pure(value)  # type: ignore

    def bind(self: 'WriterStr[V]', kleisli: 'Callable[[V], WriterStr[T]]') -> 'WriterStr[T]':
        return super().bind(kleisli)  # type: ignore

    def apply(self: 'WriterStr[Callable[[R], S]]', ma: 'WriterStr[R]') -> 'WriterStr[S]':
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        return super().apply(ma)  # type: ignore

    @classmethod
    def liftM(cls, f: Callable[[R], S], a: 'WriterStr[R]') -> 'WriterStr[S]':
        # fmap :: a -> b -> ma -> mb
        return super().liftM(f, a)  # type: ignore


class WriterList(_Writer[V], Generic[V]):
    """Monoid: List with concatenation"""
    # Actual implementation needed
    @staticmethod
    def _monoid_id() -> list[T]:
        return []

    @staticmethod
    def _monoid_operation(a: list[T], b: list[T]) -> list[T]:
        return a + b

    @classmethod
    def tell(cls, log: list[T]) -> 'WriterList[Any]':
        return WriterList(None, log)

    # For type hint purpose
    @classmethod
    def pure(cls, value: V) -> 'WriterList[V]':
        return super().pure(value)  # type: ignore

    def bind(self: 'WriterList[V]', kleisli: 'Callable[[V], WriterList[T]]') -> 'WriterList[T]':
        return super().bind(kleisli)  # type: ignore

    def apply(self: 'WriterList[Callable[[R], S]]', ma: 'WriterList[R]') -> 'WriterList[S]':
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        return super().apply(ma)  # type: ignore

    @classmethod
    def liftM(cls, f: Callable[[R], S], a: 'WriterList[R]') -> 'WriterList[S]':
        # fmap :: a -> b -> ma -> mb
        return super().liftM(f, a)  # type: ignore

class WriterSum(_Writer[V], Generic[V]):
    """Monoid: Number with sum"""
    # Actual implementation needed
    @staticmethod
    def _monoid_id() -> numeric:
        return 0

    @staticmethod
    def _monoid_operation(a: numeric, b: numeric) -> numeric:
        return a + b

    @classmethod
    def tell(cls, log: numeric) -> 'WriterSum[Any]':
        return WriterSum(None, log)

    # For type hint purpose
    @classmethod
    def pure(cls, value: V) -> 'WriterSum[V]':
        return super().pure(value)  # type: ignore

    def bind(self: 'WriterSum[V]', kleisli: 'Callable[[V], WriterSum[T]]') -> 'WriterSum[T]':
        return super().bind(kleisli)  # type: ignore

    def apply(self: 'WriterSum[Callable[[R], S]]', ma: 'WriterSum[R]') -> 'WriterSum[S]':
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        return super().apply(ma)  # type: ignore

    @classmethod
    def liftM(cls, f: Callable[[R], S], a: 'WriterSum[R]') -> 'WriterSum[S]':
        # fmap :: a -> b -> ma -> mb
        return super().liftM(f, a)  # type: ignore

class WriterProd(_Writer[V], Generic[V]):
    """Monoid: Number with sum"""
    # Actual implementation needed
    @staticmethod
    def _monoid_id() -> numeric:
        return 1

    @staticmethod
    def _monoid_operation(a: numeric, b: numeric) -> numeric:
        return a * b

    @classmethod
    def tell(cls, log: numeric) -> 'WriterProd[Any]':
        return WriterProd(None, log)

    # For type hint purpose
    @classmethod
    def pure(cls, value: V) -> 'WriterProd[V]':
        return super().pure(value)  # type: ignore

    def bind(self: 'WriterProd[V]', kleisli: 'Callable[[V], WriterProd[T]]') -> 'WriterProd[T]':
        return super().bind(kleisli)  # type: ignore

    def apply(self: 'WriterProd[Callable[[R], S]]', ma: 'WriterProd[R]') -> 'WriterProd[S]':
        # ap :: (Monad m) => m (a -> b) -> m a -> m b
        return super().apply(ma)  # type: ignore

    @classmethod
    def liftM(cls, f: Callable[[R], S], a: 'WriterProd[R]') -> 'WriterProd[S]':
        # fmap :: a -> b -> ma -> mb
        return super().liftM(f, a)  # type: ignore
