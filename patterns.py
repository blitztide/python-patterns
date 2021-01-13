#!/usr/bin/python3
"""
Title: Exploit pattern creator
Author: blitztide
Date: 10/01/2021
Version: 1
Description: Generate/search sequential sequence for use in BOF.
The pattern is a block of 3 characters  A B and C where:
[ABC][ABC][ABC]
    A -> A-Z
    B -> 0-9
    C -> a-z
"""
import sys, argparse

parser = argparse.ArgumentParser(description="Python pattern tools")
parser.add_argument("mode",default="C", help="C for create, O for offset")
parser.add_argument("positional", help="Create - Size, Offset - EIP value")
parser.add_argument("-b",help="Bad Characters", required=False)
parser.add_argument("-n",help="Number of NOP instructions", required=False)
parser.add_argument("-e",help="EIP value",required=False)
parser.add_argument("-o",help="Offset value",type=int,required=False)
parser.add_argument("-v",help="verbose", action="store_true")
args = parser.parse_args()

def convert_to_hex(string):
    if "0x" in string:
        return bytearray.fromhex(string[2:]) #Return byte array
    return string

def create(size):
    charcode=41
    buffer = ""
    for x in range(size):
        position = chr((x % 3)+65)  #Selects position within argument, 0 -> A 1 -> B 2 -> C
        block = x//3 #Returns block number of x
        if position == "A": #Increment every 260th block bound to A-Z
            buffer += chr((block//260 % 26)+65)
        if position == "B": #Increment Every 26th block bound to 0-9
            buffer += chr((block//26 % 10)+48)
        if position == "C":
            buffer += chr((block % 26)+97)  #Increment every block set to a-z
    return buffer

def offset(chars):
    buffer = ""
    largestsize = 0
    # Search for capital letter in EIP, determine largest offset size
    for x in chars:
        if x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            lettersize=(ord(x)-64)*260*3 #Finds current capital letter size
            if lettersize > largestsize: #If current size is larger than stored largest size, set largest size to letter size.
                largestsize = lettersize
        buffer = create(largestsize) #Creates the smallest pattern where search string could reside.
    for y in range(0,largestsize):   #Sliding 4 byte search using little endian
        if buffer[y] == chars[3]:
            if buffer[y+1] == chars[2]:
                if buffer[y+2] == chars[1]:
                    if buffer[y+3] == chars[0]:
                        return int(y) #Only return when all 4 bytes match
                    continue
                continue
            continue
        continue

def badchars(size,chars):   # Generate a buffer with all possible characters, then append with 0x41 characters
    for x in range(0,256):
        if not chr(x) in convert_to_hex(args.b): # Ignore all badchars specified in badchars argument
            buffer += chr(x)
    buffer += b"\x41" * (int(size)-len(buffer))
    return buffer

def exploit(size,nops,shellcode,EIP,offset): # Create a buffer which is: [PADDING][EIP][NOPSLED][SHELLCODE][PADDING]
    nopsled = b"\x90" * int(nops)   # Create nopsled to desired size
    eip_val = bytearray(EIP) # Get EIP value
    buffer = eip_val + nopsled + shellcode # Create Exploit buffer
    post_padding_size = size - offset - int(nops) - len(shellcode) - 4   #Finds the amount of post-padding required
    buffer = "A" * offset + buffer
    buffer += "A" * post_padding_size
    return buffer


def main():    # Mode selection routine.
    if (args.mode == "C"):
        if(args.v):
            print("Creating pattern of size: " + args.positional)
        print(create(int(args.positional)))
    if (args.mode == "O"):
        if args.v:
            print("Finding offset of: " + args.positional)
        print(offset(convert_to_hex(args.positional)))
    if (args.mode == "B"):
        if args.v:
            print("Generating Bad Pattern of size: " + args.positional)
        sys.stdout.write(badchars(args.positional, args.b))
    if (args.mode == "E"):
        shellcode = sys.stdin.read()
        sys.stdout.write(exploit(int(args.positional),int(args.n),shellcode,convert_to_hex(args.e),args.o))
        


if __name__ == "__main__":
    main()
