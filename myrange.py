from __future__ import annotations
from typing import final, Sequence, SupportsIndex, Iterator, overload


@final
class myrange(Sequence[int]):
    """myrange(stop) -> myrange object myrange(start, stop[, step]) -> myrange object"""
    __start: SupportsIndex
    __stop: SupportsIndex
    __step: SupportsIndex

    @property
    def start(self) -> int:
        return self.__start

    @property
    def stop(self) -> int:
        return self.__stop

    @property
    def step(self) -> int:
        return self.__step

    @overload
    def __init__(self, __stop: SupportsIndex, /) -> None:
        """
        Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step. myrange(i, j) produces i, i+1, i+2, ..., j-1. start defaults to 0, and stop is omitted! myrange(4) produces 0, 1, 2, 3. These are exactly the valid indices for a list of 4 elements. When step is given, it specifies the increment (or decrement).
        """

    @overload
    def __init__(self, __start: SupportsIndex, __stop: SupportsIndex, __step: SupportsIndex = 1, /) -> None:
        """
        myrange(stop) -> myrange object myrange(start, stop[, step]) -> myrange object

        Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step. myrange(i, j) produces i, i+1, i+2, ..., j-1. start defaults to 0, and stop is omitted! myrange(4) produces 0, 1, 2, 3. These are exactly the valid indices for a list of 4 elements. When step is given, it specifies the increment (or decrement).
        """
    
    def __init__(self, __start: SupportsIndex, __stop: SupportsIndex = None, __step: SupportsIndex = 1, /) -> None:
        self.__start = __start if __stop is not None else 0
        self.__stop = __stop if __stop is not None else __start
        if not __step:
            raise ValueError(f'{self.__class__.__name__}() arg 3 must not be zero')
        self.__step = __step
    
    def count(self, __value: int) -> int:
        """rangeobject.count(value) -> integer -- return number of occurrences of value"""
        return super().count(__value)
    
    def index(self, __value: int) -> int:
        if __value not in self:
            raise ValueError(f'{__value} is not in {self.__class__.__name__}')
        return super().index(__value)
    
    def __len__(self) -> int:
        """Return len(self)."""
        __len = (self.__stop - self.__start) // self.__step + (1 if (self.__stop - self.__start) % self.__step else 0)
        return __len if __len > 0 else 0
    
    def __contains__(self, __key: object) -> bool:
        """Return key in self."""
        return super().__contains__(__key)
    
    def __iter__(self) -> Iterator[int]:
        """Implement iter(self)."""
        __item = self.__start
        while __item < self.__stop if self.__step > 0 else __item > self.__stop:
            yield __item
            __item += self.__step
    
    @overload
    def __getitem__(self, __key: SupportsIndex) -> int:
        """Return self[key]."""
    
    @overload
    def __getitem__(self, __key: slice) -> myrange:
        """Return self[key]."""

    def __getitem__(self, __key: SupportsIndex | slice) -> int | myrange:
        def __getitem(__key: int) -> int:
            if -self.__len__() > __key >= self.__len__():
                raise IndexError(f'{self.__class__.__name__} object index out of range')
            
            if __key >= 0:
                return self.__start + self.__step * __key
            else:
                return (self.__len__() * self.__step + self.__start) + self.__step * __key
        
        if isinstance(__key, (SupportsIndex, int)):
            return __getitem(__key)
        
        # get slice values
        __start = __key.start or 0
        __stop = __key.stop if __key.stop is not None else -1
        if not (__step := __key.step if __key.step is not None else 1):
            raise ValueError('slice step cannot be zero')
        
        if -self.__len__() > __start >= self.__len__() or -self.__len__() > __stop >= self.__len__():
            raise IndexError(f'{self.__class__.__name__} object index out of range')
        
        return myrange(__getitem(__start), __getitem(__stop), self.__step * __step)
    
    def __reversed__(self) -> Iterator[int]:
        """Return a reverse iterator."""
        __item = (self.__len__() * self.__step + self.__start) - self.__step
        while __item >= self.__start if self.__step > 0 else __item <= self.__start:
            yield __item
            __item -= self.__step

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__start}, {self.__stop}%s)' % (f', {self.__step}' if self.__step != 1 else '')
