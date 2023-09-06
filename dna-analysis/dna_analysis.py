# Name: ...
# CSE 160
# Homework 2: DNA analysis

# This program reads in DNA sequencer output and computes statistics, such as
# the GC content, AT content, nucleotide counts, etc.  Run it from the command
# line like this:
#   python dna_analysis.py myfile.fastq
#
# For teaching purposes, a few more comments than normal have been added in
# to explain in detail what some Python constructs are doing.

# The sys module supports reading files, command-line arguments, etc.
import sys


# Function to convert the contents of dna_filename into a string of nucleotides
def filename_to_string(dna_filename):
    """
    dna_filename - the name of a file in expected file format
    Expected file format is: Starting with the second line of the file,
    every fourth line contains nucleotides.
    The function will read in all lines from the file containing nucleotides,
    concatenate them all into a single string, and return that string.
    """

    # YOU DO NOT NEED TO MODIFY THIS FUNCTION.

    # Creates a file object from which data can be read.
    inputfile = open(dna_filename)

    # String containing all nucleotides that have been read from the file so
    # far.
    seq = ""

    # The current line number (= the number of lines read so far).
    line_num = 0

    for line in inputfile:
        line_num = line_num + 1
        # if we are on the 2nd, 6th, 10th line...
        if line_num % 4 == 2:
            # Remove the newline characters from the end of the line
            line = line.rstrip()
            # Concatenate this line to the end of the current string
            seq = seq + line
    # close file
    inputfile.close()
    return seq


# Function to return GC Classification
def classify(gc_content):
    if gc_content > 0.58:
        classification = "high"
    elif 0.35 <= gc_content <= 0.58:
        classification = "moderate"
    else:
        classification = "low"
    return classification


###########################################################################
# Main program begins here
#

# Check if the user provided an argument
if len(sys.argv) < 2:
    print("You must supply a file name as an argument when running this "
          "program.")
    sys.exit(2)

# Save the 1st argument provided by the user, as a string.
# Note: sys.argv[0] is the name of the program itself (dna_analysis.py)
file_name = sys.argv[1]

# Open the file and read in all nucleotides into a single string of letters
nucleotides = filename_to_string(file_name)

###
# Compute statistics
###

# YOUR CODE GOES BELOW THIS POINT

# Total nucleotides seen so far.
total_count = 0

# Number of G and C nucleotides seen so far.
gc_count = 0
at_count = 0

for base in nucleotides:
    total_count = total_count + 1

    # OK to change this code!
    if base == 'C' or base == 'G':
        gc_count = gc_count + 1
    elif base == 'A' or base == 'T':
        at_count = at_count + 1

a_count = 0
c_count = 0
g_count = 0
t_count = 0
for base in nucleotides:
    if base == 'A':
        a_count = a_count + 1
    elif base == 'C':
        c_count = c_count + 1
    elif base == 'G':
        g_count = g_count + 1
    elif base == 'T':
        t_count = t_count + 1


sum_counts = g_count + c_count + a_count + t_count

gc_content = float(gc_count) / (sum_counts)
at_content = float(at_count) / (sum_counts)

print('GC-content:', gc_content)
print('AT-content:', at_content)

print("G count:", g_count)
print("C count:", c_count)
print("A count:", a_count)
print("T count:", t_count)

print("Sum of G+C+A+T counts:", sum_counts)

total_count
print("Total count:", total_count)

len_nuc = len(nucleotides)
print("Length of nucleotides:", len_nuc)

atgc_ratio = (a_count + t_count) / (g_count + c_count)
print("AT/GC Ratio:", atgc_ratio)

print("GC Classification:", classify(gc_content))

# You can add more assertions here to check properties that you think
# should be true about your results. If the condition listed is false,
# then the given message will be printed.
assert total_count == len(nucleotides), "total_count != length of nucleotides"