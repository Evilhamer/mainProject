import copy


class PrototypeMixin: # прототип
    def clone(self):

        return copy.deepcopy(self)
