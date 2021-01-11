#!/usr/bin/python3
"""
Title: Exploit pattern creator
Author: blitztide
Date: 10/01/2021
Version: 1
Description: Generate/search sequential sequence for use in BOF.
The pattern is a block of 3 characters  A B and C where:
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
        #Is 0x12312312312 format
        # Split string into 2 nibble chunks
        hexarray = b""
        for x in range(2,len(string),2):
            hexarray += chr(int(string[x]+string[x+1],16))
        return hexarray #Return byte array
    return string

def create(size):
    charcode=41
    buffer = ""
    for x in range(size):
        position = chr((x % 3)+65)  #Selects position within argument ("Makes it easier to understand")
        block = x//3 #Floor of x/3
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
            largestsize=(ord(x)-64)*260*3 #Finds Largest Capital Letter
        buffer = create(largestsize) #Creates the searchspace
    for y in range(0,largestsize):
        if buffer[y] == chars[3]:
            if buffer[y+1] == chars[2]:
                if buffer[y+2] == chars[1]:
                    if buffer[y+3] == chars[0]:
                        return int(y)
                    continue
                continue
            continue
        continue

def badchars(size,chars):
    buffer = b"\x41" * (int(size)-256-20)
    for x in range(0,256):
        if not chr(x) in convert_to_hex(args.b):
            buffer += chr(x)
    buffer += "D" * 20 #Easily see end of buffer in debugger.
    return buffer

def exploit(size,nops,shellcode,EIP,offset):
    nopsled = b"\x90" * int(nops)
    eip_val = bytearray(EIP)
    buffer = eip_val + nopsled + shellcode
    post_padding_size = size - offset - int(nops) - len(shellcode) - 4   #Finds the amound of post-padding required
    buffer = "A" * offset + buffer
    buffer += "A" * post_padding_size
    return buffer


def main():
    if (args.mode == "C"):
        if(args.v):
            print ("Creating pattern of size: " + args.positional)
        print(create(int(args.positional)))
    if (args.mode == "O"):
        if args.v:
            print("Finding offset of: " + args.positional)
        print(offset(args.positional))
    if (args.mode == "B"):
        if args.v:
            print("Generating Bad Pattern of size: " + args.positional)
        sys.stdout.write(badchars(args.positional, args.b))
    if (args.mode == "E"):
        shellcode = sys.stdin.read()
        sys.stdout.write(exploit(int(args.positional),int(args.n),shellcode,convert_to_hex(args.e),args.o))
        

   



if __name__ == "__main__":
    main()
