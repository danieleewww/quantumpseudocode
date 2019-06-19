import random

import cirq

import quantumpseudocode as qp
from .coherent_mul import init_mul, init_square


def assert_squares_correctly(n1: int, n2: int, v: int):
    final_state = qp.testing.sim_call(
        init_square,
        factor=qp.IntBuf.raw(val=v, length=n1),
        clean_out=qp.IntBuf.raw(val=0, length=n2))

    assert final_state == qp.ArgsAndKwargs([], {
        'factor': v,
        'clean_out': v**2 % 2**n2
    })


def assert_multiplies_correctly(n1: int, n2: int, n3: int, v1: int, v2: int):
    final_state = qp.testing.sim_call(
        init_mul,
        factor1=qp.IntBuf.raw(val=v1, length=n1),
        factor2=qp.IntBuf.raw(val=v2, length=n2),
        clean_out=qp.IntBuf.raw(val=0, length=n3))

    assert final_state == qp.ArgsAndKwargs([], {
        'factor1': v1,
        'factor2': v2,
        'clean_out': v1 * v2 % 2**n3
    })


def test_init_square():
    for _ in range(10):
        n1 = random.randint(0, 20)
        n2 = random.randint(0, 3*n1)
        v = random.randint(0, 2**n1 - 1)
        assert_squares_correctly(n1, n2, v)


def test_init_mul():
    for _ in range(10):
        n1 = random.randint(0, 20)
        n2 = random.randint(0, 20)
        n3 = random.randint(0, n1 + n2 + 5)
        v1 = random.randint(0, 2**n1 - 1)
        v2 = random.randint(0, 2**n2 - 1)
        assert_multiplies_correctly(n1, n2, n3, v1, v2)


def test_init_square_circuit():
    with qp.Sim(phase_fixup_bias=True, enforce_release_at_zero=False):
        with qp.LogCirqCircuit() as circuit:
            with qp.qmanaged_int(bits=2, name='f') as factor:
                with qp.qmanaged_int(bits=4, name='s') as out:
                        init_square(factor=factor, clean_out=out)
    cirq.testing.assert_has_diagram(circuit, r"""
_add_carry_in: --------X-------@---------------------------------------------------------------@---@-------X-------X-------@-------------------------------@---@-------X---
                       |       |                                                               |   |       |       |       |                               |   |       |
_sqr_offset[0]: ---X---|-------|---------------@---@---X---@---X-------@---@-------------------|---|-------|---X---|-------|-------------------------------|---|-------|---
                   |   |       |               |   |   |   |   |       |   |                   |   |       |   |   |       |                               |   |       |
_sqr_zero: --------|---|-------|---@---@---X---X---|---@---|---@---@---|---X---X-------@---@---|---|-------|---|---|-------|---@---@---X---X-------@---@---|---|-------|---
                   |   |       |   |   |   |       |   |   |   |   |   |       |       |   |   |   |       |   |   |       |   |   |   |   |       |   |   |   |       |
f[0]: -------------@---@---@---X---X---|---@-------|---|---|---|---|---|-------@---@---|---X---X---|---@---@---@---|-------|---|---|---|---|-------|---|---|---|-------|---
                   |       |   |       |   |       |   |   |   |   |   |       |   |   |       |   |   |       |   |       |   |   |   |   |       |   |   |   |       |
f[1]: -------------@-------|---|-------|---|-------|---|---|---|---|---|-------|---|---|-------|---|---|-------@---@---@---X---X---|---@---@---@---|---X---X---|---@---@---
                           |   |       |   |       |   |   |   |   |   |       |   |   |       |   |   |               |   |       |   |   |   |   |       |   |   |
s[0]: ---------------------X---@-------|---|-------|---|---|---|---|---|-------|---|---|-------@---X---X---------------|---|-------|---|---|---|---|-------|---|---|-------
                                       |   |       |   |   |   |   |   |       |   |   |                               |   |       |   |   |   |   |       |   |   |
s[1]: ---------------------------------X---@-------|---|---|---|---|---|-------@---X---X-------------------------------|---|-------|---|---|---|---|-------|---|---|-------
                                                   |   |   |   |   |   |                                               |   |       |   |   |   |   |       |   |   |
s[2]: ---------------------------------------------X---@---|---@---X---X-----------------------------------------------X---@-------|---|---|---|---|-------@---X---X-------
                                                           |                                                                       |   |   |   |   |
s[3]: -----------------------------------------------------X-----------------------------------------------------------------------X---@---@---X---X-----------------------
""", use_unicode_characters=False)