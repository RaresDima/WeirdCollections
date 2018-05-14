class MyList:
        """
        Implements the same behaviours a classic list would, but does not use any list or tuple for storage.
        """

        def __init__(self, elements = tuple()):
                self.__len = 0
                self.extend(elements)

        def __validateindex__(self, index):
                if type(index) is not int:
                        raise TypeError(f'Indices must be ints or slices. Found type {type(index)}.')
                if not abs(index) < self.__len:
                        raise IndexError(f'Index out of range. Index range [0, {self.__len - 1}]. Found {index}.')
                if index < 0:
                        index += self.__len
                return index

        def __len__(self):
                return self.__len

        def __getitem__(self, index):
                if type(index) is slice:
                        return self.__getslice__(index)
                else:
                        index = self.__validateindex__(index)
                        return getattr(self, f'__item__{index}')

        def __setitem__(self, index, value):
                if type(index) is slice:
                        return self.__setslice__(index, value)
                else:
                        index = self.__validateindex__(index)
                        setattr(self, f'__item__{index}', value)

        def __delitem__(self, index):
                if type(index) is slice:
                        self.__delslice__(index)
                else:
                        index = self.__validateindex__(index)
                        for i in range(index+1, self.__len):
                                setattr(self, f'__item__{i-1}', getattr(self, f'__item__{i}'))
                        self.__len -= 1

        def __getslice__(self, slc):
                res = MyList()
                for index in range(*slc.indices(self.__len)):
                        res.append(self.__getitem__(index))
                return res

        def __setslice__(self, slc, values):
                if not hasattr(values, '__iter__'):
                        raise AttributeError(f'<{values}> is not a sequence that '
                                             f'supports iteration over its elements.')
                start, stop, step = slc.indices(self.__len)
                expected = stop - start if step == 1 else ((stop - start - 1) // step + 1)
                if len(values) != expected:
                        raise IndexError(f'Given sequence of values has incorrect number of values. '
                                         f'Expected {expected} values. Found {len(values)} values.')
                values = iter(values)
                for index in range(*slc.indices(self.__len)):
                        self.__setitem__(index, next(values))

        def __delslice__(self, slc: slice):
                for i in reversed(range(*slc.indices(self.__len))):
                        self.__delitem__(i)
                self.__len -= len(range(*slc.indices(self.__len)))

        def append(self, value):
                setattr(self, f'__item__{self.__len}', value)
                self.__len += 1

        def extend(self, values):
                if not hasattr(values, '__iter__'):
                        raise AttributeError(f'<{values}> is not a sequence that '
                                             'supports iteration over its elements.')
                for value in values:
                        self.append(value)

        def __add__(self, other):
                res = MyList(self)
                res.extend(other)
                return res

        class __MyListIter:
                def __init__(self, my_list):
                        self.__list = my_list
                        self.__index = -1

                def __next__(self):
                        self.__index += 1
                        if self.__index == len(self.__list):
                                raise StopIteration
                        else:
                                return self.__list[self.__index]

        def __iter__(self):
                return self.__MyListIter(self)

        def __contains__(self, item):
                for element in self:
                        if element == item:
                                return True
                else:
                        return False

        def contains(self, item):
                return item in self

        def find(self, item):
                for index, element in enumerate(self):
                        if element == item:
                                return index
                else:
                        return -1

        def __str__(self):
                res = 'MyList['
                for i in range(self.__len - 1):
                        res = f'{res}{repr(self.__getitem__(i))}, '
                res = f'{res}{repr(getattr(self, f"__item__{self.__len - 1}"))}]'
                return res


l = MyList([1, 2, 3])

l.append('a')
l.append('b')
l.append('c')
l.append(3.5)
l.append(4.5)
l.append(5.5)

l[0] += 9
l[1] *= 10
l[2] = 25

print('l               = ', l)
print('len(l)          = ', len(l))
print('l[3]            = ', l[3])
print('l[-3]           = ', l[-3])
print('l[2:7:2]        = ', l[2:7:2])
print('l[::-1]         = ', l[:-1])
print('l[:-7]          = ', l[:-7])
print('l[-7:6]         = ', l[-7:6])

# print(l['abc'])
# print(l[999])
# print(l[-1000])

print('l.contains(3.5) = ', l.contains(3.5))
print('3.5 in l        = ', 3.5 in l)
print('l.contains(35)  = ', l.contains(35))
print('35 in l         = ', 35 in l)
print('l.find(3.5)     = ', l.find(3.5))
print('l.find(35)      = ', l.find(35))

l[2:5] = [0, 0, 0]
print(f'\nEXECUTED: l[2:5] = [0, 0, 0]\n\n'
      f'l = {l}')

l[2:7:2] = MyList([200, 300, 400])
print(f'\nEXECUTED: l[2:7:2] = MyList([200, 300, 400])\n\n'
      f'l = {l}')

# l[2:5] = [1, 1]
# l[2:5] = [1, 1, 1, 1, 1, 1, 1]

del l[3]
print(f'\nEXECUTED: del l[3]\n\n'
      f'l = {l}')

del l[3:8:2]
print(f'\nEXECUTED: del l[3:8:2]\n\n'
      f'l = {l}')

l.extend([-1, -2])
print(f'\nEXECUTED: l.extend([-1, -2])\n\n'
      f'l = {l}')

l.extend(MyList([-3, -4]))
print(f'\nEXECUTED: l.extend(MyList([-3, -4]))\n\n'
      f'l = {l}')

# l.extend(5)

l = l + MyList([0.1, 0.2, 0.3]) + [-0.1, -0.2, -0.3]
print(f'\nEXECUTED: l = l + MyList([0.1, 0.2, 0.3]) + [-0.1, -0.2, -0.3]\n\n'
      f'l = {l}')

# l = l + MyList([0.1, 0.2, 0.3]) + 25


print(f'\nElements of l:')
for element in l:
        print(f' * {element}')

