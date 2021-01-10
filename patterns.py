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
parser.add_argument("-v",help="verbose", action="store_true")
args = parser.parse_args()

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
        print(x)
        if x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            largestsize=(ord(x)-64)*260*3 #Finds Largest Capital Letter
        buffer = create(largestsize) #Creates the searchspace
    for y in range(0,largestsize):
        if buffer[y] == chars[0]:
            if buffer[y+1] == chars[1]:
                if buffer[y+2] == chars[2]:
                    if buffer[y+3] == chars[3]:
                        return int(y)
                    continue
                continue
            continue
        continue


def main():
    if (args.mode == "C"):
        if(args.v):
            print ("Creating pattern of size: " + args.size)
        print(create(int(args.positional)))
    if (args.mode == "O"):
        if args.v:
            print("Finding offset of: " + args.positional)
        print(offset(args.positional))
   



if __name__ == "__main__":
    main()