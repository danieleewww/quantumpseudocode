import random

import quantumpseudocode as qp


def test_vs_emulation():
    with qp.Sim(enforce_release_at_zero=False) as sim:
        bits = 4
        with qp.qmanaged_int(bits=bits, name='lvalue') as lvalue:
            for _ in range(10):
                sim.randomize_location(lvalue)

                old_state = sim.snapshot()
                op = qp.PlusEqualProduct(
                    lvalue=lvalue,
                    quantum_factor=random.randint(0, 1 << bits),
                    const_factor=random.randint(0, 1 << bits))
                op.emit_ops(qp.QubitIntersection.ALWAYS)
                op.mutate_state(sim_state=sim, forward=False)
                assert sim.snapshot() == old_state
