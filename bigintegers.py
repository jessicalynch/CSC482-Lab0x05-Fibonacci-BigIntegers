import re


class BigIntegerString:
    """Decimal string representation of big integers"""

    # Disable dynamic attribute assignment
    __slots__ = ['value']

    def __init__(self, decimal_str):
        for s in decimal_str:
            if (ord(s) - 48) not in range(0, 10):
                raise ValueError("Error: input string digits must be 0-9")
        self.value = decimal_str

    def __add__(self, other):
        """Overloads plus operator"""
        if isinstance(other, int):
            return self.plus(BigIntegerString(str(other)))
        else:
            return self.plus(other)

    def __radd__(self, other):
        """Overloads reverse add for sum() to work"""
        if isinstance(other, int):
            return BigIntegerString(str(other)).plus(self)
        else:
            return other.plus(self)

    def __mul__(self, other):
        """Overloads times operator"""
        return self.times(other)

    @property
    def abbreviated_value(self):
        """Returns abbreviated value string"""
        if len(self.value) < 12:
            return self.value
        else:
            return self.value[:5] + "..." + self.value[-5:]

    def plus(self, value_to_add):
        """Adds two BigIntegerString values together"""
        if not isinstance(value_to_add, BigIntegerString):
            raise ValueError("Plus error: param must be BigIntegerString object")
        a = self.value
        b = value_to_add.value
        c = ""

        # Pad shorter string with zeros
        if len(a) < len(b):
            a = a.zfill(len(b))
        elif len(b) < len(a):
            b = b.zfill(len(a))

        # Reverse strings to process
        # least significant digits first
        a = a[::-1]
        b = b[::-1]

        carry = 0
        for i in range(len(a)):
            # Convert ASCII characters to integers and add together
            dA = ord(a[i]) - 48
            dB = ord(b[i]) - 48
            digit_sum = dA + dB + carry

            # Carry the 1
            carry = int(digit_sum / 10)
            digit_sum = digit_sum % 10

            # Insert digit to beginning of return string
            c = chr(digit_sum + 48) + c
        if carry:
            c = str(carry) + c

        return BigIntegerString(c)

    def times(self, multiplier):
        """Multiplies two BigIntegerString values together"""
        if not isinstance(multiplier, BigIntegerString):
            raise ValueError("Times error: param must be BigIntegerString object")
        a = self.value
        b = multiplier.value

        # Reverse strings to process
        # least significant digits first
        a = a[::-1]
        b = b[::-1]

        product = BigIntegerString("0")
        num_zeros = 0

        for i in range(len(b)):
            c = "".zfill(num_zeros)
            carry = 0
            dB = ord(b[i]) - 48

            # Multiply current b digit with every digit in a
            for j in range(len(a)):
                dA = ord(a[j]) - 48
                digit_product = dB * dA + carry

                # Carry the remainder
                carry = int(digit_product / 10)
                digit_product = digit_product % 10

                # Insert digit to beginning of return string
                c = chr(digit_product + 48) + c
            if carry:
                c = str(carry) + c

            num_zeros += 1
            product = product + BigIntegerString(c)

        return product


class BigIntegerArray:
    """Array representation of big integers"""

    # Disable dynamic attribute assignment
    __slots__ = ['value', 'base', 'byte', 'hex_table']

    def __init__(self, hex_string):
        # Base used for integer array digits
        self.base = 2 ** 32

        # Number of input string characters per big int digit
        self.byte = 8

        # Generate hex table for hex char to int conversions
        self.hex_table = BigIntegerArray.generate_hex_table()

        # Convert input hex string to integer array
        self.value = self.str_to_array(hex_string)

    def __add__(self, other):
        """Overloads plus operator"""
        if isinstance(other, int):
            return self.plus(BigIntegerArray(hex(other)[2:]))
        else:
            return self.plus(other)

    def __radd__(self, other):
        """Overloads reverse add for sum() to work"""
        if isinstance(other, int):
            return BigIntegerArray(hex(other)[2:]).plus(self)
        else:
            return other.plus(self)

    def __mul__(self, other):
        """Overloads times operator"""
        return self.times(other)

    def plus(self, value_to_add):
        """Adds two BigIntegerArray values together"""
        if not isinstance(value_to_add, BigIntegerArray):
            raise ValueError("Plus error: param must be BigIntegerArray object")

        a = self.value
        b = value_to_add.value
        c = []  # Value to be assigned to BigIntegerArray return object

        # Pad shorter list with zeros
        if len(a) < len(b):
            deficit = len(b) - len(a)
            a = [0] * deficit + a
        elif len(b) < len(a):
            deficit = len(a) - len(b)
            b = [0] * deficit + b

        # Reverse strings to process
        # least significant digits first
        a = a[::-1]
        b = b[::-1]

        carry = 0
        for i in range(len(a)):
            digit_sum = a[i] + b[i] + carry

            # Carry the 1
            carry = int(digit_sum / self.base)
            digit_sum = digit_sum % self.base

            # Insert digit to beginning of return list
            c.insert(0, digit_sum)

        if carry:
            c.insert(0, carry)

        ret = BigIntegerArray("")
        ret.value = c
        return ret

    def times(self, multiplier):
        """Multiplies two BigIntegerArray values together"""
        if not isinstance(multiplier, BigIntegerArray):
            raise ValueError("Times error: param must be BigIntegerArray object")
        a = self.value
        b = multiplier.value

        # Reverse lists to process
        # least significant digits first
        a = a[::-1]
        b = b[::-1]

        product = BigIntegerArray("0")
        num_zeros = 0

        for i in range(len(b)):
            c = [0] * num_zeros
            carry = 0

            # Multiply current b digit with every digit in a
            for j in range(len(a)):
                digit_product = b[i] * a[j] + carry

                # Carry the remainder
                carry = int(digit_product / self.base)
                digit_product = digit_product % self.base

                # Insert digit to beginning of return list
                c.insert(0, digit_product)
            if carry:
                c.insert(0, carry)

            num_zeros += 1
            tmp = BigIntegerArray("")
            tmp.value = c
            product = product + tmp

        return product

    def str_to_array(self, str):
        """Converts hex string to a BigIntegerArray list"""
        # Remove white space and reverse string
        str = re.sub(r"\s", "", str)
        str = str[::-1]

        # Convert string to list of BYTE sized elements
        parsed_str = [str[i:i + self.byte] for i in range(0, len(str), self.byte)]

        # Put list and strings back in correct order
        parsed_str.reverse()
        parsed_str = [s[::-1] for s in parsed_str]

        # Convert hex string list to big int
        return [self.hex_to_int(s) for s in parsed_str]

    def hex_to_int(self, hex_str):
        """Converts hex char to integer"""
        ret_val = 0
        for char in hex_str:
            ret_val = (ret_val << 4 | self.hex_table[char])
        return ret_val

    def to_string(self):
        """Converts integer array to hex string"""
        hex_str = ""
        for i in self.value:
            hex_num = str(hex(i))[2:].upper()  # [2:] removes '0x'
            if len(hex_num) < self.byte:
                hex_num = hex_num.zfill(self.byte)
            hex_str += hex_num + " "
        return hex_str

    def to_int(self):
        """Converts integer array to regular integer"""
        int_val = 0
        power = len(self.value) - 1
        index = 0

        # Multiply each array digit by the
        # base raised to the appropriate power
        while power >= 0:
            int_val += self.value[index] * self.base ** power
            index += 1
            power -= 1
        return int_val

    def to_binary_list(self):
        """Converts BigIntegerArray value to binary list"""
        binary_list = []
        for v in self.value:
            digit_list = []
            while v > 0:
                digit_list.insert(0, v % 2)
                v //= 2
            binary_list += digit_list
        return binary_list

    def to_binary_string(self):
        """Returns binary string representation of BigIntegerArray"""
        return ''.join(map(str, self.to_binary_list()))

    @property
    def abbreviated_int(self):
        """Converts BigIntegerArray to int and returns abbreviated string representation"""
        int_val = str(self.to_int())
        if len(int_val) < 12:
            return int_val
        else:
            return int_val[:5] + "..." + int_val[-5:]

    @property
    def abbreviated_string(self):
        """Returns abbreviated hex string"""
        hex_str = self.to_string()
        stripped_hex_str = re.sub(r"\s", "", hex_str)
        if len(stripped_hex_str) <= self.byte * 4:
            return hex_str
        else:
            return stripped_hex_str[:self.byte] + "..." + stripped_hex_str[-self.byte:]

    @staticmethod
    def generate_hex_table():
        """Builds a case-insensitive dictionary used for """
        hex_table = {}
        for i in range(0, 10):
            hex_table[str(i)] = i
        for i in range(65, 71):  # uppercase A-F
            hex_table[chr(i)] = i - 65 + 10
        for i in range(97, 103):  # lowercase a-f
            hex_table[chr(i)] = i - 97 + 10
        return hex_table
