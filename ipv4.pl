#!/usr/bin/perl
#
## Usage:
## $ perl -e 'print join(".",unpack("C4",pack("L",$ARGV[0])))."\n"' 33670154
## 10.196.1.2
#
print join(".",unpack("C4",pack("L",$ARGV[0])))."\n"
