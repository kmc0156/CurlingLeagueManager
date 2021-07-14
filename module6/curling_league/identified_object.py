class IdentifiedObject:
    def __init__(self, oid):
        self._oid = oid

    def __eq__(self, other):
        """SPEC: two IndentifiedObjects are equal if they have the same type and the same oid"""
        return type(self) == type(other) and self._oid == other.oid

    def __hash__(self):
        """SPEC: return hash code based on object's oid"""
        return hash(self._oid)

    @property
    def oid(self):
        return self._oid

