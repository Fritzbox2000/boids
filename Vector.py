# TODO 3D/nD Vectors
import math


class Vector(object):
    """A Vector representation used for the boids, will contain alot of vector maths"""
    # In theory you can create a 1D vector with this, what they can be used for is something I am yet to work out, but

    def __init__(self, value=(0, 0)):
        """ Initialisation of vector
        :param value: int/float/list/tuple The vector, the int/float would be the size, the list would be a simple
                       representation of the vector

        :raises ValueError: When the vector created is too big or small, this will only make 2D vectors at the moment
        """
        # If passed a integer it will create an empty list of that size, would be easier to implement with a java array
        # never thought I would type that!
        if isinstance(value, int) or isinstance(value, float):
            if value < 0 or value > 2:
                raise ValueError("The Vector cannot be larger than size 2 or smaller than 0")
            # Can't use range on float, or imagine when someone would pass in a float, but you never know I guess? :/
            self._vect = [0 for i in range(int(value))]
        # If passed a list or tuple then it will take that to be the vector, kinda simple :)
        elif isinstance(value, list) or isinstance(value, tuple):
            if len(value) > 2:
                raise ValueError(f"The vector cannot be larger than size 2, Vector was passed {len(value)}")
            self._vect = list(value)

    @property
    def x(self):
        return self._vector_index_getter(0)

    @x.setter
    def x(self, value):
        self._vector_index_setter(0, value)

    @property
    def y(self):
        return self._vector_index_getter(1)

    @y.setter
    def y(self, value):
        self._vector_index_setter(1, value)

    def _vector_index_setter(self, index, value):
        if len(self._vect >= index+1):
            if not isinstance(value, int) and not isinstance(value, float):
                raise TypeError(f"Cannot have {type(value)} type in vector")
            self._vect[index] = value
        else:
            raise IndexError(f"Cannot change value at index {index} since vector has max index {len(self._vect) - 1}")

    def _vector_index_getter(self, index):
        if len(self._vect >= index + 1):
            return self._vect[index]
        else:
            raise IndexError(f"Cannot access value at index {index} since vector has max index {len(self._vect) -1}")

    # Edits the vector
    def add(self, other):
        """ Add a Vector, list/tuple or int/float to the vector """
        self._hidden_add(other, 0)

    # Creates new Vector
    def __add__(self, other):
        return Vector(self._hidden_add(other, 1))

    def __radd__(self, other):
        return self.__add__(other)

    # The mode in _hidden... methods will specify if to return a _vect value or edit the existing _vect
    # 0: edit existing
    # 1: Return a value

    def _hidden_add(self, other, mode):
        """ Spooky code that does spooky stuff behind the scenes making the code shorter :)"""
        # Add and __add__ use very similar code, but have different outcomes (returning or editing self._vect)
        # Add two vectors together
        if isinstance(other, Vector):
            # work out if other vector is same size
            if len(self._vect) == len(other._vect):
                # Now comes the fun part
                result = [x + other._vect[index] for index, x in enumerate(self._vect)]
                # Oh that was a bit less exciting than I was hoping
            else:
                raise ValueError("Cannot add Vectors of different lengths")
        # Adding vector with a list/tuple
        elif isinstance(other, list) or isinstance(other, tuple):
            if len(self._vect) == len(other):
                # Similar to the adding above ^
                result = [x + other[index] for index, x in enumerate(self._vect)]
            else:
                raise ValueError("Cannot add list/tuple to Vector of different lengths")
        # Adding a constant to each item (can't imagine when this will be used, but who knows?)
        elif isinstance(other, int) or isinstance(other, float):
            result = [x + other for x in self._vect]
        else:
            raise TypeError(f"Can't add {type(other)} type to Vector")
        if mode == 0:
            self._vect = result
        else:
            return result

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self._hidden_mul(other, 1))
        else:
            return self._hidden_mul(other, 1)

    def __rmul__(self, other):
        return self._hidden_mul(other, 1)

    def multiply_vect(self, other):
        """ Multiply the Vector by Vector or list/tuple with dot multiplication
        :param  other: Vector/list/tuple - dot product with the Vector
        :return float which is the dot product
        :raise  ValueError,TypeError"""
        if isinstance(other, Vector) or isinstance(other, list) or isinstance(other, tuple):
            return self._hidden_mul(other)
        else:
            raise TypeError(f"Can't multiply Vector with {type(other)} type")

    def scalar_multiply(self, other):
        """ Multiply the Vector by int/float with scalar multiplication
        :param other: int/float - Scalar multiple to the vector
        :raise ValueError,TypeError"""
        if isinstance(other, int) or isinstance(other, float):
            self._vect = self._hidden_mul(other)
        else:
            raise TypeError(f"Can't do scalar product with {type(other)} type")

    def _hidden_mul(self, other, mode=1, mul_type="dot"):
        """ Spooky code that does spooky stuff behind the scenes making the code shorter :)
            Unless you add 3D vectors and cross multiplication mul_type should stay untouched """
        # There are two main forms of multiplication when it comes to vectors, dot and cross
        # cross multiplication is for 3d vectors and as such won't be implemented at the moment, but I have left in code
        # to make it easy to do
        # dot multiplication is easy tho, for Vectors V and U the dot product D is defined by
        # d = (V1 x U1) + (V2 x U2) + ... + (Vn x Un)

        # The mode doesn't matter if the thing passed is an integer or float, it is then a scalar product which is EZ
        if isinstance(other, Vector):
            # Vectors are same size
            if len(self._vect) == len(other._vect):
                if mul_type == "dot":
                    # dot product multiplication
                    result = sum([x*other._vect[index] for index, x in enumerate(self._vect)])
                elif mul_type == "cross":
                    # TODO Vector Multiplication
                    result = []
                else:
                    # Wrong mul_type
                    raise ValueError(f"mul_type must be either dot or cross not {mul_type}")
            else:
                # Wrong Size
                raise ValueError(f"Can't multiply vectors of different sizes")
        # Multiplying Vector and list/float
        elif isinstance(other, list) or isinstance(other, tuple):
            # Check they are the same size
            if len(self._vect) == len(other):
                # Check type of multiplication
                if mul_type == "dot":
                    result = sum([x*other[index] for index, x in enumerate(self._vect)])
                elif mul_type == "cross":
                    # TODO Vector Multiplication
                    result = []
                else:
                    # Wrong mul_type
                    raise ValueError(f"mul_type must be either dot or cross not {mul_type}")
            else:
                # Wrong size
                raise ValueError(f"Can't multiply vector with list/float of other size")
        # Scalar multiplication
        elif isinstance(other, int) or isinstance(other, float):
            # d = (s x V1, s x V2, ..., s x Vn)
            result = [x*other for x in self._vect]
        else:
            # Wrong type of other
            raise TypeError(f"Can't Multiply {type(other)} with Vector")
        # Only time when _vect would be edited is when doing Cross product which isn't implemented due to only having 2d
        # vectors
        if mode == 0 and mul_type == "cross":
            self._vect = result
        else:
            return result

    def find_angle(self, vector):
        """ Finds the angle between two vectors
        :param vector: Vector - The Vector to be compared to the current vector

        :return Angle (in radians) between the vectors

        :raise TypeError,ValueError"""
        # standardise vectors
        vect1, vect2 = self.standardise(), vector.standardise()
        # dot product between two standardised vectors
        return math.acos(vect1 * vect2)

    def standardise(self):
        """ Standardises the vector so |V| = 1
        :return Standardised Vector"""
        mag = self.magnitude()
        # Divide all the items
        return Vector([x/mag for x in self._vect])

    def magnitude(self):
        """ The magnitude of a vector
        :return Int the magnitude of vector"""
        # Magnitude is worked out through Pythagoras' theorem
        return math.sqrt(sum([x**2 for x in self._vect]))

    def neg(self):
        return Vector([-x for x in self._vect])

    def __str__(self):
        return str(self._vect)

    def __repr__(self):
        return f"Vector{str(self._vect)}"

    def __getitem__(self, item):
        return self._vect[item]

    def __setitem__(self, key, value):
        self._vect[key] = value

    def __contains__(self, item):
        return True if item in self._vect else False

    def __copy__(self):
        return Vector(self._vect)

    def __eq__(self, other):
        return True if self._vect == other._vect else False

    def __len__(self):
        return len(self._vect)


if __name__ == '__main__':
    v1 = Vector([1, 2])
    v2 = Vector([1, 1])
    print(v1 * v2)
    print(v1.magnitude())
    print(v1.standardise())
    print(v1.find_angle(v2))
    print(v2[1])
    print(repr(v1))
    import random
    list_vect = []
    for v_num in range(100):
        list_vect.append(Vector([random.randint(-30, 30), random.randint(-30, 30)]))
    mean = sum(list_vect) * (1/100)
    print(mean)
