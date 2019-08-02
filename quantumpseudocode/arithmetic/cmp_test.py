import random

import cirq

import quantumpseudocode as qp


def test_do():
    qp.testing.assert_semi_quantum_func_is_consistent(
        qp.arithmetic.do_if_less_than,
        fuzz_space={
            'lhs': lambda: random.randint(0, 511),
            'rhs': lambda: random.randint(0, 511),
            'or_equal': [False, True],
            'effect': [qp.OP_PHASE_FLIP],
        },
        fuzz_count=100)


def test_cmp():
    with qp.Sim():
        with qp.qmanaged_int(bits=4) as t:
            t.init(2)
            with qp.hold(t >= 2) as q:
                assert qp.measure(q)
            with qp.hold(t > 2) as q:
                assert not qp.measure(q)
            with qp.hold(t <= 2) as q:
                assert qp.measure(q)
            with qp.hold(t < 2) as q:
                assert not qp.measure(q)
            assert qp.measure(t, reset=True) == 2


def test_if_less_than_then_circuit():
    with qp.Sim(enforce_release_at_zero=False):
        with qp.LogCirqCircuit() as circuit:
            with qp.qmanaged_int(bits=4, name='lhs') as lhs:
                with qp.qmanaged_int(bits=4, name='rhs') as rhs:
                    with qp.qmanaged(qp.Qubit(name='_or_eq')) as c:
                        with qp.qmanaged(qp.Qubit(name='t')) as t:
                            qp.arithmetic.do_if_less_than(
                                lhs=lhs,
                                rhs=rhs,
                                or_equal=c,
                                effect=qp.Toggle(lvalue=qp.RawQureg([t])))

    cirq.testing.assert_has_diagram(circuit, r"""
_or_eq: ---X-------@---@-------------------------------------------------------------------------------------------------------@---@-------X---
           |       |   |                                                                                                       |   |       |
lhs[0]: ---|---X---X---@-------------------------------------------------------------------------------------------------------@---X---X---|---
           |   |       |                                                                                                       |       |   |
lhs[1]: ---|---|-------|-------X---X---@-----------------------------------------------------------------------@---X---X-------|-------|---|---
           |   |       |       |   |   |                                                                       |   |   |       |       |   |
lhs[2]: ---|---|-------|-------|---|---|-------X---X---@---------------------------------------@---X---X-------|---|---|-------|-------|---|---
           |   |       |       |   |   |       |   |   |                                       |   |   |       |   |   |       |       |   |
lhs[3]: ---|---|-------|-------|---|---|-------|---|---|-------X---X---@-------@---X---X-------|---|---|-------|---|---|-------|-------|---|---
           |   |       |       |   |   |       |   |   |       |   |   |       |   |   |       |   |   |       |   |   |       |       |   |
rhs[0]: ---@---@-------X---X---|---@---@-------|---|---|-------|---|---|-------|---|---|-------|---|---|-------@---@---|---X---X-------@---@---
                           |   |       |       |   |   |       |   |   |       |   |   |       |   |   |       |       |   |
rhs[1]: -------------------@---@-------X---X---|---@---@-------|---|---|-------|---|---|-------@---@---|---X---X-------@---@-------------------
                                           |   |       |       |   |   |       |   |   |       |       |   |
rhs[2]: -----------------------------------@---@-------X---X---|---@---@-------@---@---|---X---X-------@---@-----------------------------------
                                                           |   |       |       |       |   |
rhs[3]: ---------------------------------------------------@---@-------X---@---X-------@---@---------------------------------------------------
                                                                           |
t: ------------------------------------------------------------------------X-------------------------------------------------------------------
        """, use_unicode_characters=False)
