from .xor import (
    do_xor,
    do_xor_const,
)

from .add import (
    do_addition,
    uma_sweep,
    maj_sweep,
)

from .cmp import (
    IfLessThanRVal,
    do_if_less_than,
    do_classical_if_less_than,
)

from .mul import (
    do_multiplication,
)

from .quotient import (
    do_init_small_quotient,
    do_div_rem,
)

from .mult_add import (
    do_multiply_add,
    do_classical_multiply_add,
)

from .measure import (
    measure,
    MeasureOperation,
    StartMeasurementBasedUncomputation,
    EndMeasurementBasedComputationOp,
    measurement_based_uncomputation,
)

from .lookup import (
    LookupRValue,
    do_xor_lookup,
    del_xor_lookup,
)

from .phase_flip import (
    OP_PHASE_FLIP,
    phase_flip,
    GlobalPhaseOp,
)

from .toggle import (
    cnot,
    Toggle,
)

from .unary import (
    UnaryRValue,
)

from .swap import (
    swap,
)
