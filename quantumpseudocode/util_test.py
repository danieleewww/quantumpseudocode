import quantumpseudocode as qp


def test_ceil_lg2():
    f = qp.ceil_lg2
    assert f(0) == 0
    assert f(1) == 0
    assert f(2) == 1
    assert f(3) == 2
    assert f(4) == 2
    assert f(5) == 3
    assert f(6) == 3
    assert f(7) == 3
    assert f(8) == 3
    assert f(9) == 4
    assert f((1 << 100) - 1) == 100
    assert f((1 << 100)) == 100
    assert f((1 << 100) + 1) == 101


def test_ceil_power_of_two():
    f = qp.ceil_power_of_two
    assert f(0) == 1
    assert f(1) == 1
    assert f(2) == 2
    assert f(3) == 4
    assert f(4) == 4
    assert f(5) == 8
    assert f(6) == 8
    assert f(7) == 8
    assert f(8) == 8
    assert f(9) == 16
    assert f((1 << 100) - 1) == 1 << 100
    assert f((1 << 100)) == 1 << 100
    assert f((1 << 100) + 1) == 1 << 101


def test_floor_power_of_two():
    f = qp.floor_power_of_two
    assert f(1) == 1
    assert f(2) == 2
    assert f(3) == 2
    assert f(4) == 4
    assert f(5) == 4
    assert f(6) == 4
    assert f(7) == 4
    assert f(8) == 8
    assert f(9) == 8
    assert f((1 << 100) - 1) == 1 << 99
    assert f((1 << 100)) == 1 << 100
    assert f((1 << 100) + 1) == 1 << 100


def test_little_endian_int():
    f = qp.little_endian_int
    assert f([]) == 0
    assert f([False]) == 0
    assert f([True]) == 1
    assert f([False, False]) == 0
    assert f([True, False]) == 1
    assert f([False, True]) == 2
    assert f([True, True]) == 3


def test_little_endian_bits():
    f = qp.little_endian_bits
    assert f(0, 4) == (False, False, False, False)
    assert f(3, 4) == (True, True, False, False)
    assert f(5, 4) == (True, False, True, False)
    assert f(5, 6) == (True, False, True, False, False, False)


def test_floor_lg2():
    f = qp.floor_lg2
    assert f(1) == 0
    assert f(2) == 1
    assert f(3) == 1
    assert f(4) == 2
    assert f(5) == 2
    assert f(6) == 2
    assert f(7) == 2
    assert f(8) == 3
    assert f(9) == 3
    assert f((1 << 100) - 1) == 99
    assert f((1 << 100)) == 100
    assert f((1 << 100) + 1) == 100


def test_leading_zero_bit_count():
    f = qp.leading_zero_bit_count
    assert f(-3) == 0
    assert f(-2) == 1
    assert f(-1) == 0
    assert f(0) is None
    assert f(1) == 0
    assert f(2) == 1
    assert f(3) == 0
    assert f(4) == 2
    assert f(5) == 0
    assert f(6) == 1
    assert f(7) == 0
    assert f(8) == 3
    assert f(9) == 0
    assert f((1 << 100) - 2) == 1
    assert f((1 << 100) - 1) == 0
    assert f((1 << 100)) == 100
    assert f((1 << 100) + 1) == 0
