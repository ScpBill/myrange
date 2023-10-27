from __future__ import annotations
from typing import final, Sequence, SupportsIndex, Iterator, overload, Self, Tuple


@final
class myrange(Sequence[int]):
    """myrange(stop) -> myrange object myrange(start, stop[, step]) -> myrange object"""

    @property
    def start(self) -> int: return self.__start
    @property
    def stop(self) -> int:  return self.__stop
    @property
    def step(self) -> int:  return self.__step
    
    @overload
    def __new__(cls, __stop: SupportsIndex) -> Self:
        """
        Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step. myrange(i, j) produces i, i+1, i+2, ..., j-1. start defaults to 0, and stop is omitted! myrange(4) produces 0, 1, 2, 3. These are exactly the valid indices for a list of 4 elements. When step is given, it specifies the increment (or decrement).
        """
    
    @overload
    def __new__(cls, __start: SupportsIndex, __stop: SupportsIndex, __step: SupportsIndex = ...) -> Self:
        """
        myrange(stop) -> myrange object myrange(start, stop[, step]) -> myrange object

        Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step. myrange(i, j) produces i, i+1, i+2, ..., j-1. start defaults to 0, and stop is omitted! myrange(4) produces 0, 1, 2, 3. These are exactly the valid indices for a list of 4 elements. When step is given, it specifies the increment (or decrement).
        """

    def __new__(cls, *args: Tuple[int]) -> Self:
        def _isinteger(n: object) -> int:
            if isinstance(n, (int, SupportsIndex)):
                return n.__index__()
            raise TypeError(f"'{n.__class__.__name__}' object cannot be interpreted as an integer")

        this = super().__new__(cls)
        match args:
            case ():
                raise TypeError(f'{cls} expected at least 1 argument, got 0')
            case stop,:
                this.__start = 0
                this.__stop = _isinteger(stop)
                this.__step = 1

            case start, stop, *other:
                if len(other) > 1:
                    raise TypeError(f'{cls.__name__} expected at most 3 arguments, got {2+len(other)}')
                step, = other or (1,)
                if not step:
                    raise ValueError(f'{cls.__name__}() arg 3 must not be zero')

                this.__start = _isinteger(start)
                this.__stop = _isinteger(stop)
                this.__step = _isinteger(step)

        this.__slots__ = ()
        return this
    
    def count(self, __value: int) -> int:
        """rangeobject.count(value) -> integer -- return number of occurrences of value"""
        return int(__value in self)
    
    def index(self, __value: int) -> int:  # type: ignore[override]
        """rangeobject.index(value) -> integer -- return index of value. Raise ValueError if the value is not present."""
        if __value not in self:
            raise ValueError(f'{__value} is not in {self.__class__.__name__}')
        return (__value - self.start) // self.step
    
    def __len__(self) -> int:
        """Return len(self)."""
        __len = (self.stop - self.start) // self.step + (1 if (self.stop - self.start) % self.step else 0)
        return __len if __len > 0 else 0
    
    def __contains__(self, __key: object) -> bool:
        """Return key in self."""

        try:  # Getting rid of numbers with digits after the decimal point or non-numbers
            assert hasattr(__key, '__int__')
            if not isinstance(__key, int):
                assert hash(__key) == hash(int(__key))
                __key = int(__key)
        except (ValueError, AssertionError):
            return False
        
        if self.start <= __key < self.stop if self.step > 0 else self.start >= __key > self.stop:
            return (__key - self.start) % self.step == 0
        return False
    
    def __iter__(self) -> Iterator[int]:
        """Implement iter(self)."""
        item = self.start
        while item < self.stop if self.step > 0 else item > self.stop:
            yield item
            item += self.step
    
    @overload
    def __getitem__(self, __key: int) -> int:
        """Return self[key]."""
    
    @overload
    def __getitem__(self, __key: slice) -> myrange:
        """Return self[key]."""

    def __getitem__(self, __key: int|slice) -> int|myrange:
        def __getitem(__key: int) -> int:
            if -self.__len__() > __key >= self.__len__():
                raise IndexError(f'{self.__class__.__name__} object index out of range')
            
            if __key >= 0:
                return self.start + self.step * __key
            else:
                return (self.__len__() * self.step + self.start) + self.step * __key
        
        if isinstance(__key, int):
            return __getitem(__key)
        
        # Getting the slice values
        start = __key.start if __key.start is not None else  0
        stop  = __key.stop  if __key.stop  is not None else -1
        step  = __key.step  if __key.step  is not None else  1
        if not step:
            raise ValueError('slice step cannot be zero')
        
        if -self.__len__() > start >= self.__len__() or -self.__len__() > stop >= self.__len__():
            raise IndexError(f'{self.__class__.__name__} object index out of range')
        
        return myrange(__getitem(start), __getitem(stop), self.step * step)
    
    def __reversed__(self) -> Iterator[int]:
        """Return a reverse iterator."""
        item = (self.__len__() * self.step + self.start) - self.step
        while item >= self.start if self.step > 0 else item <= self.start:
            yield item
            item -= self.step

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.start}, {self.stop}%s)' % (f', {self.step}' if self.step != 1 else '')

    def __repr__(self) -> str:
        return self.__str__()
    
    # TODO (1): Узнать способ генерации хэша оригинального класса и применить здесь
    def __hash__(self) -> int:
        return hash((self.start, self.stop, self.step))
    
    # TODO (2): Сделать проверку по хэшам
    def __eq__(self, __value: object) -> bool:
        return isinstance(
            __value, myrange  # true if object type is myrange and ...
        ) and (
            (__value.start, __value.stop) == (self.start, self.stop)  # ... the start and stop values are equal and ...
        ) and (
            __value.step == self.step or __value.__len__() == self.__len__()  # ... is equal to either the step value or the length
        )
    
    # TODO (2): Сделась проверку по хэшам
    def __ne__(self, __value: object) -> bool:
        return not isinstance(
            __value, myrange  # true if object type not is myrange or ...
        ) or (
            (__value.start, __value.stop) != (self.start, self.stop)  # ... the start and stop values are not equal or ...
        ) or (
            __value.step != self.step and __value.__len__() != self.__len__()  # ... the step and length values are not equal either
        )


if __name__ == '__main__':
    pass
