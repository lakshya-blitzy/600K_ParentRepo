"""Application entry point for the numeric aggregation demo.

Builds a fixed list of numbers (``[10, 20, 30, 40]``), computes their
total using the computation library (``service.calculate_total``), and
prints the results to standard output. The program is deterministic:
the fixed input always produces ``Total: 100``.

This module is self-contained and synchronous. It has no third-party
dependencies and imports only the local ``service`` module.

Run:
    python app.py

Expected output:
    Total: 100
    10
    20
    30
    40
    Application completed

Source: app.py:L1-L16
"""
from service import calculate_total

def main():
    """Orchestrate the aggregation workflow and print results to stdout.

    Constructs the fixed input list ``[10, 20, 30, 40]``, computes its
    total via ``service.calculate_total`` (always ``100`` for this fixed
    input), then prints ``Total: <total>`` (that is, ``Total: 100``),
    followed by each number on its own line, and finally the
    ``Application completed`` line.

    This function takes no arguments. Its only effects are the console
    messages written to standard output via ``print()``.

    Returns:
        None: ``main`` returns nothing; it communicates solely through
        console side effects.

    Source: app.py:L3-L13
    """
    numbers = [10, 20, 30, 40]

    total = calculate_total(numbers)

    print(f"Total: {total}")

    for number in numbers:
        print(number)

    print("Application completed")

if __name__ == "__main__":
    main()
