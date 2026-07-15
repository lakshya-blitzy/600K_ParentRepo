"""Computation library for numeric aggregation.

Provides the numeric helper functions used by the application entry
point (``app.py``). Two public functions are exported:

    * ``calculate_total(numbers)`` -- sum an iterable of numbers.
    * ``calculate_average(numbers)`` -- arithmetic mean of an iterable.

The module is self-contained, synchronous, and has no third-party
dependencies.

Source: service.py:L1-L14
"""


def calculate_total(numbers):
    """Return the sum of an iterable of numbers.

    Args:
        numbers: Iterable of numeric values (e.g., a list of ints or
            floats) to add together.

    Returns:
        The accumulated total of all elements. Returns ``0`` for an
        empty iterable.

    Note:
        No type checking is performed; passing a non-iterable or a
        non-numeric argument raises the corresponding built-in
        exception at runtime.

    Source: service.py:L1-L7
    """
    total = 0

    for number in numbers:
        total += number

    return total


def calculate_average(numbers):
    """Return the arithmetic mean of an iterable of numbers.

    Args:
        numbers: Iterable of numeric values to average.

    Returns:
        The arithmetic mean, computed as
        ``calculate_total(numbers) / len(numbers)``. Returns ``0`` when
        ``numbers`` is empty or otherwise falsy; the guard short-circuits
        before the division, so an empty input never triggers a
        ZeroDivisionError.

    Source: service.py:L10-L14
    """
    if not numbers:
        return 0

    return calculate_total(numbers) / len(numbers)
