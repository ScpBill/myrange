# myrange
A copy of an existing `range` object written in python for python

## What is it

`(class) range`
---
range(stop) -> range object range(start, stop[, step]) -> range object

Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step. range(i, j) produces i, i+1, i+2, ..., j-1. start defaults to 0, and stop is omitted! range(4) produces 0, 1, 2, 3. These are exactly the valid indices for a list of 4 elements. When step is given, it specifies the increment (or decrement).
```py
# default object
for i in range(100):
    print(i)

# myrange object
for i in myrange(100):
    print(i)
```
```py
>>> myrange(10)  # view as string
myrange(0, 10)
>>> next(myrange(10))  # object is not an iterator
TypeError: 'range' object is not an iterator
```

## Tests & Functional
```py
def speedometer(func) -> None:
    """Decorator for measuring the speed of function execution"""
    def decorator(obj: range | myrange):
        last = time.time()
        func(obj)
        print(f'Test of {obj.__name__} last for {time.time() - last} seconds')
    return decorator


@speedometer
def test(func: range | myrange) -> None:
    """Some tests of range & myrange objects"""

    # let's check how quickly the object is iterated
    for _ in func(-1000000, 1000000, 3): pass

    # let's make a slice in the object with non-standard values
    obj = func(500, -300, -3)[11:-11:2]

    # find out which number is exactly contained in the object
    print(['this: %s' % i if i in obj else i for i in func(11)])


def main():
    test(range)
    test(myrange)
```

## Results of test
```
[0, 1, 2, 3, 4, 'this: 5', 6, 7, 8, 9, 10]                                                                                                                                         
Test of range last for 0.038524627685546875 seconds
[0, 1, 2, 3, 4, 'this: 5', 6, 7, 8, 9, 10]
Test of myrange last for 0.14751911163330078 seconds
```
