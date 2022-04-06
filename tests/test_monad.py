import pytest
from funcpy.maybe import Maybe, Just, Nothing
from funcpy.functions import curry, filterM, mapM
from funcpy.list import List
from funcpy.writer import *


def satisfy_monad_law(monad, test_val=11) -> bool:
    satisfied = True

    def kleisli1(x: int):
        return monad.pure(x ** 2)

    def kleisli2(x: int):
        return monad.pure(-x)

    # Left identity
    if not monad.pure(test_val).bind(kleisli1) \
           == kleisli1(test_val):
        satisfied = False
    # Right identity
    if not monad.pure(test_val).bind(monad.pure) \
           == monad.pure(test_val):
        satisfied = False
    # Associativity
    if not monad.pure(test_val).bind(kleisli1).bind(kleisli2) \
           == monad.pure(test_val).bind(lambda x: kleisli1(x).bind(kleisli2)):
        satisfied = False
    return satisfied


@pytest.mark.parametrize("input_monad", [
    Maybe,
    List,
    WriterStr,
    WriterList,
    WriterSum,
    WriterProd,
])
def test_monad_law(input_monad):
    assert satisfy_monad_law(input_monad)


@pytest.mark.parametrize("maybe_test_input, maybe_expected", [
    # Monadic Laws
    # Left identity
    (Maybe.pure(7).bind(lambda x: Just(x + 1)),
     Just(8)),
    # Right identity

    # __str__, __eq__
    (Just(2) == Nothing,
     False),
    (str(Just(2)),
     "Just 2"),
    (str(Nothing),
     "Nothing"),
    # pure test
    (Maybe.pure(2),
     Just(2)),
    # fmap test
    # fmap :: (a -> b) -> f a -> f b
    (Maybe.liftM(lambda x: x + 1, Just(1)),
     Just(2)),
    (Maybe.liftM(lambda x: x + 1, Nothing),
     Nothing),
    # bind test
    # (>>=) :: m a -> (a -> m b) -> m b
    (Just(1).bind(lambda x: Just(x + 1)),
     Just(2)),
    (Nothing.bind(lambda x: Just(x + 1)),
     Nothing),
    # apply test
    # ap :: (Monad m) => m (a -> b) -> m a -> m b
    (Maybe.pure(lambda x: x + 1).apply(Just(1)),
     Just(2)),
    (Maybe.pure(lambda x: x + 1).apply(Nothing),
     Nothing),
    # filterM test
    # filterM :: (a -> m Bool) -> [a] -> m [a]
    (filterM(lambda x: Just(True) if x > 5 else Just(False), [2, 4, 6, 8, 10]),
     Just([6, 8, 10])),
    (filterM(lambda x: Nothing if x > 5 else Just(False), [2, 4, 6, 8, 10]),
     Nothing),
    # mapM test
    # mapM :: (a -> m b) -> [a] -> m [a]
    (mapM(lambda x: Just(str(x)), [1, 2, 3, 4, 5]),
     Just(['1', '2', '3', '4', '5'])),
    (mapM(lambda x: Just(str(x)) if x > 1 else Nothing, [1, 2, 3, 4, 5]),
     Nothing)
])
def test_maybe(maybe_test_input, maybe_expected):
    assert maybe_test_input == maybe_expected


@pytest.mark.parametrize("list_test_input, list_expected", [
    # __iter__, len, str
    (list(iter(List([1, 2, 3]))),
     [1, 2, 3]),
    (len(List([1, 2, 3])),
     3),
    (str(List([1, 2, 3])),
     "List [1, 2, 3]"),
    # pure test
    (List.pure(2),
     [2]),
    # fmap test
    # fmap :: (a -> b) -> f a -> f b
    (List.liftM(lambda x: x + 1, List([1, 2, 3, 4, 5])),
     List([2, 3, 4, 5, 6])),
    # bind test
    # (>>=) :: m a -> (a -> m b) -> m b
    (List([1, 2, 3]).bind(lambda x: List([x + 1, x - 1])),
     [2, 0, 3, 1, 4, 2]),
    # apply test
    # ap :: (Monad m) => m (a -> b) -> m a -> m b
    (List.pure(lambda x: str(x)).apply(List([1, 2, 3, 4, 5])),
     ['1', '2', '3', '4', '5']),
    # filterM test
    # filterM :: (a -> m Bool) -> [a] -> m [a]
    (filterM(lambda _: List([True, False]), [1, 2, 3]),
     [[1, 2, 3], [2, 3], [1, 3], [3], [1, 2], [2], [1], []]),
])
def test_list(list_test_input, list_expected):
    assert list_test_input == list_expected


@pytest.mark.parametrize("writer_test_input, writer_expected", [
    (WriterStr.pure(5).bind(lambda x: WriterStr(x + 1, "Added 1")),
     WriterStr(6, "Added 1")),
    (WriterList.pure(5).bind(lambda x: WriterList(x + 1, ["Added 1"])).bind(lambda x: WriterList(x + 2, ["Added 2"])),
     WriterList(8, ["Added 1", "Added 2"])),
    (WriterStr.pure(1).bind(
        lambda x: WriterStr.pure(2).bind(
            lambda y: WriterStr.tell("Added 1, 2").bind(
                lambda _: WriterStr.pure(x + y)))),
     WriterStr(3, "Added 1, 2"))
])
def test_writer(writer_test_input, writer_expected):
    assert writer_test_input == writer_expected
