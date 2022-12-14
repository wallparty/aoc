from collections import deque
from functools import partial
from itertools import chain, islice, tee
from operator import getitem, methodcaller
from typing import Any, Callable, Iterable, Iterator, TypeVar

S = TypeVar("S")
T = TypeVar("T")


def group_amounts(iterator: Iterator[T], n: int) -> Iterator[Iterator[T]]:
    """Generate groups of items of size n.

    Args
    ----
        iterator (Iterator[T]): the iterator.
        n (int): size of group to create.

    Raises
    ------
        ValueError: for n < 2.

    Yields
    ------
        Iterator[Iterator[T]]: an iterator of grouped iterators.
    """
    if n < 2:
        raise ValueError("n must be >= 2")

    while (i := next(iterator, None)) is not None:
        yield chain([i], islice(iterator, n - 1))


def map_to_dict(d: dict[S, T], iterator: Iterator[S]) -> Iterator[T]:
    """Map an iterator to a dictionary's keys.

    Args
    ----
        d (dict[S, T]): the dictionary to map into.
        iterator (Iterator[S]): the iterator.

    Yields
    ------
        Iterator[T]: an iterator made of the dictionary's values.
    """
    from_d: partial[T] = partial(getitem, d)
    return map(from_d, iterator)


def consume(iterator: Iterator[T], n: int | None = None) -> None:
    """Advance the iterator n-steps ahead. If n is None, consume entirely.

    From itertools recipes:
    https://docs.python.org/3/library/itertools.html#itertools-recipes

    Args
    ----
        iterator (Iterator[T]): iterator to consume.
        n (int, optional): number of steps to consume by. Defaults to None.
    """
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def iter_len(iterator: Iterator[T]) -> tuple[Iterator[T], int]:
    """Calculate the length of an iterator.

    Args
    ----
        iterator (Iterator[T]): the iterator to calculate length for.

    Returns
    -------
        tuple[Iterator[T], int]: the original iterator and its length.
    """
    returned_iterator, length_iterator = tee(iterator)
    return (returned_iterator, sum(1 for _ in length_iterator))


def call_method(method: Callable[..., T]) -> Callable[[S], T]:
    """Call the method of a class.

    Args
    ----
        method (Callable[..., T]): the reference to the class method.

    Returns
    -------
        Callable[[S], T]: a callable that will call the method.
    """
    return methodcaller(method.__name__)


def call_with(*args: Any, **kwargs: Any) -> Callable[..., T]:
    """Prepare a call to a function with given arguments.

    Returns
    -------
        Callable[..., T]: a callable that will call the function it is given as input.
    """

    def caller(fn: Callable[..., T]) -> T:
        return fn(*args, **kwargs)

    return caller


def ingest_while(
    predicate: Callable[[T], Any], iterator: Iterator[T]
) -> Iterator[None]:
    """Ingest the elements of an iterator whilst a predicate is true.

    Args
    ----
        predicate (Callable[[T], Any]): the predicate to check each element against.
        iterator (Iterator[T]): the iterator.

    Yields
    ------
        Iterator[None]: an iterator of None values.
    """
    while (elem := (next(iterator, None))) is not None:
        if predicate(elem):
            yield None
        else:
            break


def transpose(iterator: Iterator[Iterable[T]]) -> Iterator[Iterable[T]]:
    """Transpose an iterator of iterables.

    For example, for an iterator i yielding [(1, "a"), (2, "b"), (3, "c")], the
    transpose(i) will yield ([1, 2, 3], ["a", "b", "c"]).

    Args
    ----
        iterator (Iterator[Iterator[T]]): the iterator to transpose.

    Yields
    ------
        Iterator[Iterator[T]]: the transposed iterator.
    """
    return zip(*iterator)
