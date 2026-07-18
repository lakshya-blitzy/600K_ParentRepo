"""Parity tests for the pure computation module (service.py).

These verify that calculate_total and calculate_average behave exactly as in
the original console application; they must never alter behavior.
"""
from service import calculate_total, calculate_average


def test_calculate_total_fixed_input():
    assert calculate_total([10, 20, 30, 40]) == 100


def test_calculate_total_empty():
    assert calculate_total([]) == 0


def test_calculate_average_fixed_input():
    result = calculate_average([10, 20, 30, 40])
    assert result == 25.0
    assert isinstance(result, float)


def test_calculate_average_empty_is_integer_zero():
    result = calculate_average([])
    # Value AND type invariant: empty-input average is the integer 0, not 0.0.
    assert result == 0
    assert type(result) is int
