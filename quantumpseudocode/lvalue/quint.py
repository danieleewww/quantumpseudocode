import cirq

import quantumpseudocode as qp


@cirq.value_equality
class Quint:
    def __init__(self, qureg: 'qp.Qureg'):
        self.qureg = qureg

    def _value_equality_values_(self):
        return self.qureg

    def __len__(self):
        return len(self.qureg)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.qureg[item]
        return Quint(self.qureg[item])

    def init(self,
             value: 'qp.RValue[int]',
             controls: 'qp.QubitIntersection' = None):
        value.init_storage_location(self,
                                    controls or qp.QubitIntersection.EMPTY)

    def clear(self,
              value: 'qp.RValue[int]',
              controls: 'qp.QubitIntersection' = None):
        value.del_storage_location(self,
                                   controls or qp.QubitIntersection.EMPTY)

    def __setitem__(self, key, value):
        if value != self[key]:
            raise NotImplementedError(
                "quint.__setitem__ is only for syntax like q[0] ^= q[1]. "
                "Don't know how to write {!r} into quint {!r}.".format(
                    value, key))

    def __mul__(self, other):
        if isinstance(other, int):
            return qp.ScaledIntRValue(self, other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __le__(self, other):
        return qp.IfLessThanRVal(qp.rval(self),
                                    qp.rval(other),
                                    qp.rval(True))

    def __lt__(self, other):
        return qp.IfLessThanRVal(qp.rval(self),
                                    qp.rval(other),
                                    qp.rval(False))

    def __ge__(self, other):
        return qp.IfLessThanRVal(qp.rval(other),
                                    qp.rval(self),
                                    qp.rval(False))

    def __gt__(self, other):
        return qp.IfLessThanRVal(qp.rval(other),
                                    qp.rval(self),
                                    qp.rval(True))

    def __ixor__(self, other):
        if isinstance(other, int):
            qp.emit(qp.OP_XOR_C(self, other))
            return self

        if isinstance(other, Quint):
            qp.emit(qp.OP_XOR(self, other))
            return self

        rev = getattr(other, '__rixor__', None)
        if rev is not None:
            return rev(self)

        return NotImplemented

    def __iadd__(self, other):
        rev = getattr(other, '__riadd__', None)
        if rev is not None:
            return rev(self)

        # Constant addition.
        if isinstance(other, (int, qp.IntRValue)):
            known = other.val if isinstance(other, qp.IntRValue) else other
            if known == 0:
                return self
            k = qp.leading_zero_bit_count(known)
            qp.emit(qp.PlusEqual(lvalue=self[k:],
                                 offset=known >> k,
                                 carry_in=False))
            return self

        # Register addition.
        if isinstance(other, (Quint, qp.RValue)):
            qp.emit(qp.PlusEqual(lvalue=self,
                                 offset=other,
                                 carry_in=False))
            return self

        return NotImplemented

    def __isub__(self, other):
        with qp.invert():
            return self.__iadd__(other)

    def __str__(self):
        return str(self.qureg)

    def __repr__(self):
        return 'qp.Quint({!r})'.format(self.qureg)
