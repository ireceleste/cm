# !/usr/bin/env python

# Copyright (C) 2022 Irene Celestino

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
First assignment for the CMEPDA course, 2022/23.
--- Goal
Write a Python program that prints the relative frequence of each letter
of the alphabet (without distinguishing between lower and upper case) in the
book.

--- Specifications
 - the program should have a --help option summarizing the usage
 - the program should accept the path to the input file from the command line
 - the program should print out the total elapsed time
 - the program should have an option to display a histogram of the frequences
 - [optional] the program should have an option to print out the basic book
   stats (e.g., number of characters, number of words, number of lines, etc.)
"""

import time
import argparse
import matplotlib.pyplot as plt


def process(file_path: str):
    """
    Create a dictionary with frequency of letters in file_path.

    (optional) Shows histogram and/or prints book statistics
    """
    print(f'Opening input file {file_path}...')

    with open(file_path, 'r') as input_file:
        text = input_file.read()
        text = text.lower()  # sets all letters to lower case
        # print(text)
        print('Reading of the file completed')

# Initializing all variables
    dictionary = {chr(i): 0 for i in range(ord('a'), ord('z')+1)}
    n_spaces = 0
    n_newline = 0
    n_characters = len(text)
    n_lines = 0


# for loop on text to count letters/stats
    for i, char in enumerate(text):
        if char in dictionary:
            dictionary[char] += 1
        elif char == chr(32):  # counting spaces
            n_spaces += 1
        elif char == '\n':  # counting number of lines
            n_lines += 1
            if text[i-1] != '\n':
                n_newline += 1  # counting number of new line after a word

    print("Number of occurrences for each letter: ", dictionary)

# Settings for the histogram figure
    plt.figure(1)
    plt.title('Histogram relative frequence of each letter')
    plt.xlabel('Letter')
    plt.ylabel('Number of occurrences')
    plt.bar(dictionary.keys(), dictionary.values(),
            align='center', color='orange')


# Prinnt elapsed time
    t_f = time.time()
    print(f'Total elapsed time : {t_f-t0} s')

# Optional commands
    show_histogram = input("\nShow histogram? [yes/no]: ")
    print_stats = input("\nPrint Statistics? [yes/no]: ")

    if print_stats == "yes":
        print('\nBook Statistics:')
        print(f'\n Number of characters = {n_characters}')
        print(f'Number of words = {n_spaces+n_newline}')
        print(f'Number of lines = {n_lines}')

    if show_histogram == "yes":
        plt.show()


if __name__ == '__main__':
    t0 = time.time()
    parser = argparse.ArgumentParser(description='Print some book statistics')
    parser.add_argument('infile', type=str, help='path to the input file')
    # parser.add_argument('--infile', type=str, help='path to the input file',
    #                    default="pride_prejudice.txt")
    args = parser.parse_args()
    process(args.infile)
