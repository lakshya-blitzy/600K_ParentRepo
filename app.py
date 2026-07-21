"""Parent repository entry-point application.

This module is the direct-execution entry point for the parent repository. It
computes and prints the total of a fixed list of numbers using the local
``service`` module: the summation is delegated to
:func:`service.calculate_total`, after which the total, each individual number,
and a final completion message are written to standard output.

Run it directly with ``python app.py``; see the :func:`main` docstring for the
exact standard-output the program produces.

Source: app.py
"""

from service import calculate_total

def main():
    """Entry point that sums a hard-coded list and prints the results.

    Builds the fixed list ``[10, 20, 30, 40]``, delegates the summation to
    :func:`service.calculate_total`, prints ``Total: 100``, then prints each
    number on its own line, and finally prints ``Application completed``.

    Args:
        None.

    Returns:
        None: results are written to standard output.

    Source: app.py:L3
    """
    numbers = [10, 20, 30, 40]

    total = calculate_total(numbers)

    print(f"Total: {total}")

    # Print each input number in order, one per line; the summation itself is delegated to service.calculate_total.
    for number in numbers:
        print(number)

    print("Application completed")

# Invoke main() only when run directly (e.g., python app.py), not when imported, so imports stay side-effect free.
if __name__ == "__main__":
    main()
