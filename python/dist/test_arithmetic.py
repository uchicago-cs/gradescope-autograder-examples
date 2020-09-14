import sys
import pytest

import arithmetic


@pytest.mark.category("addition")
def test_addition_1():
    x = arithmetic.add(5, 7)

    assert x == 12


@pytest.mark.category("addition")
def test_addition_2():
    x = arithmetic.add(-4, -5)

    assert x == -9


@pytest.mark.category("addition")
def test_addition_3():
    x = arithmetic.add(6, 0)

    assert x == 6


@pytest.mark.category("addition")
def test_addition_4():
    x = arithmetic.add(0, 0)

    assert x == 0


@pytest.mark.category("addition")
def test_addition_5():
    x = arithmetic.add(0, -5)

    assert x == -5


@pytest.mark.category("multiplication")
def test_multiplication_1():
    x = arithmetic.multiply(5, 7)

    assert x == 35


@pytest.mark.category("multiplication")
def test_multiplication_2():
    x = arithmetic.multiply(-4, -5)

    assert x == 20


@pytest.mark.category("multiplication")
def test_multiplication_3():
    x = arithmetic.multiply(4, -5)

    assert x == -20    


@pytest.mark.category("multiplication")
def test_multiplication_4():
    x = arithmetic.multiply(0, 100)

    assert x == 0


@pytest.mark.category("multiplication")
def test_multiplication_5():
    x = arithmetic.multiply(1, 100)

    assert x == 100    