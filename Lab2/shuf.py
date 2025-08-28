#!/usr/bin/python

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys, argparse

class shuffle:
    def __init__(self, contents):
        #assign self and shuffle the contents
        self.lines = contents
        random.shuffle(self.lines)

    def chooseline(self): #select with replacement
        return random.choice(self.lines)

    def getShuf(self): #return shuffled lines
        return self.lines

def main():
    parser = argparse.ArgumentParser(
        prog='shuf',
        description='Write a random permutation of the input lines to standard output.'
    )
    
    parser.add_argument('-e', '--echo', nargs='*', metavar='ARG', help='treat each ARG as an input line')
    parser.add_argument('-i', '--input-range', type=str, metavar='LO-HI', help='treat each number LO through HI as an input line')
    parser.add_argument('-n', '--head-count', type=int, metavar='COUNT', help='output at most COUNT lines')
    parser.add_argument('-r', '--repeat', action='store_true', help='output lines can be repeated')
    parser.add_argument('filename', nargs='?', metavar='FILE', help='input file. With no FILE, or when FILE is -, read standard input.')
    args = parser.parse_args(sys.argv[1:]) #parse arguments and removes script name

    ##########################################
    # Cannot combine -e and -i
    if args.echo != None and args.input_range != None:
        parser.error("cannot combine -e and -i options")
    
    # Cannot use -i with a file (except for '-') (-e doesn't count because it will treat it as strings
    if args.filename != None and args.input_range != None:
        parser.error(f"extra operand ‘{args.filename}’")
    
    # preparing contents as a list
    if args.echo is not None:
        contents = args.echo
    elif args.input_range is not None:
        try:
            lo_str, hi_str = args.input_range.split('-')
            lo = int(lo_str)
            hi = int(hi_str)
            if lo > hi + 1: # check if invalid range input
                parser.error(f"invalid input range: ‘{lo}-{hi}’")
            #contents = list(range(lo, hi + 1)) #range is inclusive
            contents = [str(i) for i in range (lo, hi + 1)]
        except:
            parser.error("unexpected error: input-range")
    elif args.filename == '-' or args.filename == None:
        try:
            contents = sys.stdin.readlines()
        except:
            parser.error("I/O Error: stdin failure")
    else:
        try:
            f = open(args.filename, 'r')
            contents = f.readlines()
            f.close()
        except IOError as e:
            errno, strerror = e.args
            parser.error("I/O error({0}): {1}".
                     format(errno, strerror))
    if args.head_count != None and args.head_count < 0:
        parser.error(f"invalid line count: ‘{args.head_count}’")

    #print(contents)
    contents = [line.rstrip('\n') for line in contents]
    #print(contents)
    if len(contents) == 0:
        parser.error("no lines to repeat")

    permu = shuffle(contents)
    if args.repeat:
        if args.head_count != None:
            for i in range(args.head_count):
                print(permu.chooseline())
        else:
            try:
                while True:
                    print(permu.chooseline())
            except KeyboardInterrupt:
                pass
    else:
        lines = permu.getShuf()
        if args.head_count != None:
            for i in range(args.head_count):
                print(lines[i])
        else:
            for line in permu.getShuf():
                print(line)
    
if __name__ == "__main__":
    main()
