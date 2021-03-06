# python-patterns
Python implementation of patterns and offsets for fuzzing and buffer overflows.

![Screenshot of Python-Patterns](https://raw.githubusercontent.com/blitztide/python-patterns/main/Pattern_create.png)

## Syntax

``` python3 patterns.py [Operation] [values] ```

## Modes
### Pattern Create (Mode C)
patterns creates patterns in blocks of 3 bytes, following an upper case letter, number and lower case letter pattern (A0aA0bA0c).

``` python3 patterns.py C 1000 ```

### Offset (Mode O)
This takes an input in 0xAABBCCDD format to look for a matching pattern in a generated pattern and it will return endian-ness and offset in bytes.

``` python3 patterns.py O 0x41306141```

### Badchars (Mode B)
This mode will generate a buffer of all hex codes followed by a buffer of 0x41 characters for a specified size, bad characters can be selected with -b 0x000102

### Exploit (Mode E)
This will take shellcode from StdIn and create an output buffer of a specified size, offset, nopsled size and EIP value. It will automatically prepend append 0x41 characters to fill the specified buffer size.
