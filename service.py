"""Computation library for numeric aggregation.

Provides the numeric helper functions for the application. The entry
point (``app.py``) currently uses ``calculate_total``;
``calculate_average`` is an additional exported helper that is not used
by the CLI path. Two public functions are exported:

    * ``calculate_total(numbers)`` -- sum an iterable of numbers.
    * ``calculate_average(numbers)`` -- arithmetic mean of a sized
      collection of numbers.

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
    """Return the arithmetic mean of a sized collection of numbers.

    Args:
        numbers: A sized collection of numeric values to average, such
            as a list or tuple. When ``numbers`` is non-falsy it must
            support ``len()``, because the mean divides the sum by
            ``len(numbers)``. Unsized iterables (for example, a
            generator) are not supported and raise ``TypeError`` at the
            ``len(numbers)`` call.

    Returns:
        The arithmetic mean, computed as
        ``calculate_total(numbers) / len(numbers)``. Returns the literal
        ``0`` only when ``numbers`` is falsy (for example, an empty list
        ``[]``, empty tuple ``()``, or empty string ``""``); the
        ``if not numbers`` guard short-circuits before the division, so
        a falsy input never triggers a ``ZeroDivisionError``.

    Raises:
        TypeError: For a non-falsy argument, in either of two distinct
            ways depending on the input. An unsized iterable (for
            example, a generator) is summed successfully by
            ``calculate_total`` but then fails at the final
            ``len(numbers)`` call, which unsized iterables do not
            support. A non-iterable argument (for example, an ``int``)
            instead fails earlier, during aggregation inside
            ``calculate_total`` ("'int' object is not iterable"),
            before ``len()`` is reached.

    Source: service.py:L10-L14
    """
    if not numbers:
        return 0

    return calculate_total(numbers) / len(numbers)
