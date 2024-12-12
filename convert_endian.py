#!/usr/bin/python3

'''
Little-endian: 0x12345678
Big-endian:    0x78563412

Sample run:
[mbpatil@mbpatil scripts]$ ./convert_endian.py
Usage: ./convert_endian.py <number>
Ex: ./convert_endian.py 305419896

  input=0x12345678            305419896
 output=0x78563412            2018915346

[mbpatil@mbpatil scripts]$ ./convert_endian.py 1234
  input=0x4d2                 1234
 output=0xd204                53764

[mbpatil@mbpatil scripts]$ ./convert_endian.py 0x1234
  input=0x1234                4660
 output=0x3412                13330

[mbpatil@mbpatil scripts]$ ./convert_endian.py 1234567890
  input=0x499602d2            1234567890
 output=0xd2029649            3523384905

[mbpatil@mbpatil scripts]$ ./convert_endian.py 12345678901234567890
  input=0xab54a98ceb1f0ad2    12345678901234567890
 output=0xd20a1feb8ca954ab    15134944594269656235
'''

import sys

input = 0x12345678
output = 0

if len(sys.argv) == 1:
    print("Usage: %s <number>" % sys.argv[0])
    print("Ex: %s %d\n" % (sys.argv[0], input))
else:
    input = int(sys.argv[1], 0)

print("%8s%-20s " % ("input=", hex(input)), input);
while input:
    byte = input & 0xff
    input = input >> 8

    output = output << 8
    output = output | byte
print("%8s%-20s " % ("output=", hex(output)), output),
