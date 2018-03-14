from copy import deepcopy


class DefDict(dict):
        """
        Implements the core feature of the default dict class, returning a default value for any key that was not used,
        but also allows a model object to be given as a default, not only factory callables.
        If the default object is a callable it will be treated as a factory callable, otherwise it will be copied and
        inserted as the default value for any unused key.
        """

        def __init__(self, default, **kwargs):
                super().__init__(**kwargs)
                self._default = default

        def __getitem__(self, item):
                if item not in self:
                        super(DefDict, self).__setitem__(
                                item,
                                self._default() if hasattr(self._default, '__call__') 
                                else deepcopy(self._default))
                return super(DefDict, self).__getitem__(item)


# Using a factory function for default
dd = DefDict(list)
dd['x'] = 123
print(dd['x'])
print(dd['y'])

print('------------------')

# Using a default object
dd = DefDict([1, 2, 3])
dd['x'] = 123
dd['z'][2] = 5
print(dd['x'])
print(dd['y'])
print(dd['z'])
