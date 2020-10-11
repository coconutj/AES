# -*- coding: utf-8 -*-
"""
    Created: 10/10/2020
    Last modification: 10/11/2020

    @creator: coconutj

    Brief: Toy Implementation of Bytes for AES Cipher
"""

#-- Import --#
import functools
#- End Import -#

class Byte:
    """
    Object of a byte as a field element of F_256
    - attributes : (int) byte
    - methods : *init, *repr, *str, *eq, *ne, *add, *radd, *iadd, *mul, *rmul, *imul
    """

    def __init__(self, byte=0):
        """
        Default byte 0x00
        """
        try:
            assert type(byte) == int
            self.byte = byte
        except AssertionError:
            raise TypeError("Input not of type Bytes")

    def __repr__(self):
        """
        Controls the display in the command prompt
        - output: (str) no name
        """
        """
        if self.byte == 0:
            string = '''< Byte Object >
-------------------------
    Binary repr: 0
    Hexadecimal repr: 0
    Field repr: 0
'''
        else:
            bin_n = bin(self.byte)[2:]
            string = '''< Byte Object >
-------------------------
    Binary repr: {0}
    Hexadecimal repr: {1}
    Field repr: {2}
'''.format(bin_n, hex(self.byte)[2:], ' + '.join(['x^'+str(k) for k in range(len(bin_n)) if bin_n[::-1][k] == '1']))
        return string
        """
        return "{%02x}" % self.byte

    def __str__(self):
        """
        Controls the display through the print function
        - output: (str) no name
        """
        return repr(self)

    def __eq__(self, oth_byte):
        """
        Overload of the == operator for two Byte objects
        - input: (Byte object) oth_byte
        - output: (bool) no name
        """
        if type(oth_byte) != type(self):
            raise ValueError("You can only compare two bytes")
        else:
            return self.byte == oth_byte.byte

    def __ne__(self, oth_byte):
        """
        Overload of the != operator for two Byte objects
        - input: (Byte object) oth_byte
        - output: (bool) no name
        """
        return not(self == oth_byte)

    def __add__(self, oth_byte):
        """
        Overload of the + operator for two Byte objects
        - input: (Byte object) oth_byte
        - output: (Byte object) no_name
        """
        return Byte(self.byte ^ oth_byte.byte)

    def __radd__(self, oth_byte):
        """
        Overload of the + operator for two Byte objects (+ is commutative)
        - input: (Byte object) oth_byte
        - output: (Byte object) no_name
        """
        return self + oth_byte

    def __iadd__(self, oth_byte):
        """
        Overload of the += operator for two Byte objects
        - input: (Byte object) oth_byte
        - output: (Byte object) no_name
        """
        return self + oth_byte

    def __mul__(self, oth_byte):
        """
        Overload of the * operator for two Byte objects
        - input: (Byte object) oth_byte
        - output: (Byte object) no_name
        """
        # mul_x = lambda a: (a << 1) if (a <= 127) else ((a << 1) ^ 0x11b)
        # mul_xk = lambda a, k: a if (k == 0) else mul_xk(mul_x(a), k-1)
        mul_xk = lambda a, k: a if (k == 0) else mul_xk((a << 1) if (a <= 127) else ((a << 1) ^ 0x11b), k-1)

        lis = [mul_xk(self.byte, k) for k, bit in enumerate(bin(oth_byte.byte)[2:][::-1]) if bit == '1']

        if lis == []:
            return Byte()
        else:
            return Byte(functools.reduce(lambda a,b: a ^ b, lis))

    def __rmul__(self, oth_byte):
        """
        Overload of the * operator for two Byte objects (* is commutative)
        - input: (Byte object) oth_byte
        - output: (Byte object) no_name
        """
        return self * oth_byte

    def __imul__(self, oth_byte):
        """
        Overload of the *= operator for two Byte objects
        - input: (Byte object) oth_byte
        - output: (Byte object) no_name
        """
        return self * oth_byte


class ByteMatrix:
    """
    Matrix of Byte objects
    - attributes : (list of lists of Bytes) arr, (int) m, (int) n, (tuple) shape
    - methods : *init, *repr, *str, *eq, *ne, *add, *radd, *iadd, *mul, *imul, shape, *lshift, *rshift, *getitem, *setitem
    """

    def __init__(self, arr, m=None, n=None):
        try:
            assert (type(arr) == list)
            assert (len(arr) != 0)

            # Single list is given, input parameters m, n are used to reshape the list
            if all(map(lambda elt: type(elt) == Byte, arr)):
                # Construct a row because row number not specified
                if (m is None):
                    self.arr = [arr]
                    self.m = 1
                    self.n = len(arr)
                elif (n is None):
                    self.arr = [[byte] for byte in arr]
                    self.m = len(arr)
                    self.n = 1
                else:
                    assert len(arr) == m*n
                    self.arr = []
                    for i in range(m):
                        self.arr.append(arr[n*i:n*(i+1)])
                    self.m = m
                    self.n = n
            # List of lists is given
            elif all(map(lambda elt: type(elt) == list, arr)):
                # Verifying that all elements are of type Byte
                assert all([all(map(lambda elt: type(elt) == Byte, arr[k])) for k in range(len(arr))])
                # Verifying that all rows have the same number of elements
                len_lis = [len(arr[k]) for k in range(len(arr))]
                assert min(len_lis) == max(len_lis) 

                self.m = len(arr)
                self.n = len(arr[0])
                self.arr = arr
            else:
                assert 0 == 1
            self.shape = (self.m, self.n)
        except AssertionError:
        	raise TypeError("Given parameters are not valid.")

    def __repr__(self):
        """
        Controls the display in the command prompt
        - output: (str) string
        """
        string = "< ByteMatrix Object >\n-----------------------\n"
        for i in range(self.m):
            # string += "[ " + ' '.join(["{%02x}" % self.arr[i][j].byte for j in range(self.n)]) + " ]\n"
            string += "[ " + ' '.join([repr(self.arr[i][j]) for j in range(self.n)]) + " ]\n"
        return string

    def __str__(self):
        """
        Controls the display through the print function
        - output: (str) no name
        """
        return repr(self)

    def __eq__(self, oth_mat):
        """
        Overload of the == operator for two ByteMatrix objects
        - input: (ByteMatrix object) oth_mat
        - output: (bool) no name
        """
        return self.arr == oth_mat.arr

    def __ne__(self, oth_mat):
        """
        Overload of the != operator for two ByteMatrix objects
        - input: (ByteMatrix object) oth_mat
        - output: (bool) no name
        """
        return not(self == oth_mat)

    def __add__(self, oth_mat):
        """
        Overload of the + operator for two ByteMatrix objects
        - input: (ByteMatrix object) oth_mat
        - output: (ByteMatrix object) no name
        """
        try:
            assert (self.m == oth_mat.m) and (self.n == oth_mat.n)
            arr = []
            for i in range(self.m):
                arr.append([self.arr[i][j] + oth_mat.arr[i][j] for j in range(self.n)])
            return ByteMatrix(arr=arr, m=self.m, n=self.n)
        except AssertionError:
            raise ValueError("Dimensions don't match.")

    def __radd__(self, oth_mat):
        """
        Overload of the + operator for two ByteMatrix objects (+ is commutative)
        - input: (ByteMatrix object) oth_mat
        - output: (ByteMatrix object) no name
        """
        return self + oth_mat

    def __iadd__(self, oth_mat):
        """
        Overload of the += operator for two ByteMatrix objects
        - input: (ByteMatrix object) oth_mat
        - output: (ByteMatrix object) no name
        """
        return self + oth_mat

    def __mul__(self, oth_mat):
        """
        Overload of the * operator for a ByteMatrix and an integer
        - input: (ByteMatrix object) oth_mat
        - output: (ByteMatrix object) no name
        """
        try:
            assert (self.n == oth_mat.m)
            arr = []
            for i in range(self.m):
                for j in range(oth_mat.n):
                    S = Byte(0)
                    for k in range(self.n):
                        S += self.arr[i][k]*oth_mat.arr[k][j]
                    arr.append(S)
            # arr is reshaped by the constructor
            return ByteMatrix(arr=arr, m=self.m, n=oth_mat.n)
        except AssertionError:
            raise ValueError("Dimensions don't match.")

    def __imul__(self, n):
        """
        Overload of the *= operator for a ByteMatrix and an integer
        - input: (int) n
        - output: (ByteMatrix object) R
        """
        return self * n

    def shape(self):
        """
        Returns the shape of the ByteMatrix
        - output: (tuple) no name
        """
        return self.m, self.n

    def __lshift__(self, tup):
    	"""
    	Performs a circular left shift of given row by given step
    	- input: (tuple) tup = (row, step)
    	"""
    	try:
    		assert type(tup) == tuple
    		assert len(tup) == 2
    		row, step = tup
    		assert (type(row) == int) and (type(step) == int)
    		assert (0 <= row < self.m)

    		self.arr[row] = [self.arr[row][(j+step)%self.n] for j in range(self.n)]
    	except AssertionError:
    		raise ValueError("Operand is not valid.")

    def __rshift__(self, tup):
    	"""
    	Performs a circular right shift of given row by given step
    	- input: (tuple) tup = (row, step)
    	"""
    	try:
    		assert type(tup) == tuple
    		assert len(tup) == 2
    		row, step = tup
    		assert (type(row) == int) and (type(step) == int)
    		assert (0 <= row < self.m)

    		self.arr[row] = [self.arr[row][(j-step)%self.n] for j in range(self.n)]
    	except AssertionError:
    		raise ValueError("Operand is not valid.")

    def __getitem__(self, indices):
        """
        Overload of the [] operator to get an element
        - input: (int or tuple) indices
        - output: (Byte object) no name
        """
        # Exception are handled by list getitem method
        if type(indices) == int:
            return ByteMatrix(arr=self.arr[indices], m=1, n=self.n)
        elif type(indices) == tuple:
            try:
                assert len(indices) == 2
            except:
                raise IndexError("Too many indices were given.")
            if type(indices[0]) == int:
                if type(indices[1]) == int:
                    return self.arr[indices[0]][indices[1]]
                elif indices[1] == slice(None, None, None):
                    return ByteMatrix(arr=self.arr[indices[0]], m=1, n=self.n)
                else:
                    raise NotImplementedError("Slices are not implemented.")
            elif indices[0] == slice(None, None, None):
                if type(indices[1]) == int:
                    return ByteMatrix(arr=[self.arr[i][indices[1]] for i in range(self.m)], m=self.m, n=1)
                elif indices[1] == slice(None, None, None):
                    return self
                else:
                    raise NotImplementedError("Slices are not implemented.")
            else:
                raise NotImplementedError("Slices are not implemented.")
        else:
            raise TypeError("Indices must be integers or slices")

    def __setitem__(self, indices, value):
        """
        Overload of the [] operator to set an element
        - input: (int or tuple) indices, (Byte or ByteMatrix) value
        - output: None
        """
        # Exception are handled by list getitem method
        if type(indices) == int:
            try:
                assert type(value) == ByteMatrix
                assert (value.m == 1) and (value.n == self.n)
                self.arr[indices] = value.arr[0]
            except AssertionError:
                raise ValueError("Operand is of wrong type or wrong dimension.")
        elif type(indices) == tuple:
            try:
                assert len(indices) == 2
            except:
                raise IndexError("Too many indices were given.")

            if type(indices[0]) == int:
                if type(indices[1]) == int:
                    try:
                        assert type(value) == Byte
                        self.arr[indices[0]][indices[1]] = value
                    except AssertionError:
                        TypeError("Operand must be of type Byte.")
                elif indices[1] == slice(None, None, None):
                    try:
                        assert type(value) == ByteMatrix
                        assert (value.m == 1) and (value.n == self.n)
                        self.arr[indices[0]] = value.arr[0]
                    except AssertionError:
                        raise TypeError("Operand must be type ByteMatrix of size 1xn.")
                else:
                    raise NotImplementedError("Slices are not implemented.")

            elif indices[0] == slice(None, None, None):
                if type(indices[1]) == int:
                    try:
                        assert type(value) == ByteMatrix
                        assert (value.m == self.m) and (value.n == 1)
                        for i in range(self.m):
                            self.arr[i][indices[1]] = value[i,0]
                    except AssertionError:
                        raise TypeError("Operand must be type ByteMatrix of size mx1.")
                elif indices[1] == slice(None, None, None):
                    try:
                        assert type(value) == ByteMatrix
                        assert (value.m == self.m) and (value.n == self.n)
                        self.arr = value.arr
                    except AssertionError:
                        raise TypeError("Operand must be type ByteMatrix of same dimensions.")
                else:
                    raise NotImplementedError("Slices are not implemented.")
            else:
                raise NotImplementedError("Slices are not implemented.")
        else:
            raise TypeError("Indices must be integers or slices")

def zeros(dim):
    """
    Generates a ByteMatrix of dimension dim filled with 0 Byte objects
    - input: (tuple) dim
    - output: (ByteMatrix object) no name
    """
    try:
        assert type(dim) == tuple
        assert len(dim) == 2
        assert (type(dim[0]) == int) and (type(dim[1]) == int)
        m,n = dim
        return ByteMatrix(arr=[Byte() for i in range(m*n)], m=m, n=n)
    except AssertionError:
        raise ValueError("Dimension must be given as a 2-long tuple of integers")

def bytes2ByteMatrix(block):
    """
    Maps a 16-byte block to a 4x4 ByteMatrix object
    - input: (bytes, 16 B) block
    - output: (ByteMatrix object) state
    """
    try:
        # Padding not handled here
        assert len(block) == 16
        state = zeros((4,4))
        for j in range(4):
            for i in range(4):
                state[i,j] = Byte(block[4*j + i])
        return state
    except AssertionError:
        raise ValueError("Block should be 16 bytes. Padding is not handled.")

def ByteMatrix2bytes(state):
    """
    Maps a 4x4 ByteMatrix object to a 16-byte block
    - input: (ByteMatrix object) state
    - output: (bytes, 16 B) block
    """
    try:
        assert type(state) == ByteMatrix
        assert (state.m == 4) and (state.n == 4)
        block = b''
        for j in range(4):
            for i in range(4):
                block += bytes([state[i,j].byte])
        return block
    except AssertionError:
        raise ValueError("Argument must be of type ByteMatrix of size 4x4.")