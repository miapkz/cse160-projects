# Name Mia Pekez
# CSE 160
# Homework 3: Image Blurring

# A Python program to blur an image.

from PIL import Image
import itertools
import sys
import os


def read_image(file_path):
    """
    Reads the image file at file_path into a rectangular grid of pixels,
    represented as a list of list of integer. Each element of the outer list
    is one row of pixels, where each pixel is an integer x such that
    0 <= x < 256. Returns the grid of pixels.
    """
    # YOU DO NOT NEED TO MODIFY THIS FUNCTION.
    # Do not worry about understanding "How" this function works.
    print("Reading image", file_path)

    # Open a file in image format
    try:
        image_file = Image.open(file_path)
    except IOError as e:
        print(e)
        return
    except Exception:
        print("Unexpected error reading file", file_path)
        return

    width, height = image_file.size
    data = list(image_file.getdata())

    # data is a single list. We break it into a nested list.
    result = []
    for r in range(height):
        # Get the part of the list that corresponds to this row.
        row_start = r * width
        row = data[row_start:row_start + width]

        result.append(row)
    return result


def write_image(file_name, pixel_grid):
    """
    Given pixel_grid as an image in a list of lists of integers format,
    write it to the filename file_name as an image.
    Requires that:
    * Each row of pixel_grid is of the same length
    * Each pixel value is an integer x such that 0 <= x < 256.
    """
    # YOU DO NOT NEED TO MODIFY THIS FUNCTION.
    # Do not worry about understanding "How" this function works.
    size = len(pixel_grid[0]), len(pixel_grid)
    image = Image.new("L", size)

    print("Writing", size[0], 'x', size[1], "image to file", file_name)

    # Flatten the list by making an iterable sequence over the inner lists
    # and then materializing the whole list.
    data = list(itertools.chain.from_iterable(pixel_grid))
    image.putdata(data)

    try:
        # Write the image. File extension of file_name determines
        # the encoding.
        image.save(file_name)
    except IOError as e:
        print(e)
    except Exception:
        print("Unexpected error writing file", file_name)


def csv_line_to_list(line):
    """
    Given a CSV-formatted row of integers, returns the integers
    as a list. The argument line must be a string such as

        "255, 0,  27"

    Note that
     * There are no extra spaces at the beginning or end of
       the string, and
     * Commas are only between elements (no comma before the
       first element, and no comma after the last one).

    This method will present an error if either of these
    constraints are violated.
    """
    # YOU DO NOT NEED TO MODIFY THIS FUNCTION.
    # Do not worry about understanding "How" this function works.
    # Although it is not too tricky if you look up the string split
    # function.
    row = []
    for pixel in line.split(','):
        row.append(int(pixel))
    return row


def read_grid(file_path):
    """
    Reads the CSV file at file_path into rectangular grid of pixels,
    represented as a list of lists of integers. This method should
    read any file written by the write_grid function.  Returns the
    grid of pixels.
    """

    # open an read file
    text_file = open(file_path)
    # initialize returned list
    grid_1 = []
    # go through each line in file
    for line in text_file:
        # convert to row of integers and add to returned list
        row = csv_line_to_list(line)
        grid_1.append(row)
    return grid_1


def write_grid(file_name, pixel_grid):
    """
    Writes the given pixel_grid to filename file_name as CSV.
    """
    # YOU DO NOT NEED TO MODIFY THIS FUNCTION.
    # Do not worry about understanding "How" this function works.
    output_file = open(file_name, 'w')

    for row in pixel_grid:
        output_file.write(str(row[0]))
        for column in range(1, len(row)):
            output_file.write(', ' + str(row[column]).rjust(3))
        output_file.write('\n')

    output_file.close()


def get_pixel_at(pixel_grid, i, j):
    """
    Returns the pixel in pixel_grid at row i and column j (zero-indexed).
    Returns 0 if i or j is out of bounds for the given pixel_grid.
    Returns 0 if i or j is a negative value.
    """

    # retrieve value at index i and index j
    if i < 0 or j < 0:
        return 0
    elif i >= len(pixel_grid) or j >= len(pixel_grid[0]):
        return 0
    else:
        value = pixel_grid[i][j]
    return value


def test_get_pixel_at():
    """ Basic, brief sanity checks for get_pixel_at. """

    # If all of these tests return true, then your solution to
    # get_pixel_at is probably mostly correct. However, passing
    # these tests does not necessarily mean your solution is completely
    # correct. There are many ways to implement get_pixel_at
    # that pass these tests and are still wrong. No set of tests
    # can check every possible grid or case.

    test_grid = [
        [1, 2, 3, 4, 5, 6],
        [0, 2, 4, 6, 8, 10],
        [3, 4, 5, 6, 7, 8]
    ]

    try:
        assert get_pixel_at(test_grid, 0, 0) == 1,   \
            "Call to get_pixel_at(0, 0) should have returned 1."
        assert get_pixel_at(test_grid, -1, 0) == 0,  \
            "Call to get_pixel_at(-1, 0) should have returned 0."
        assert get_pixel_at(test_grid, 0, -1) == 0,  \
            "Call to get_pixel_at(0, -1) should have returned 0."
        assert get_pixel_at(test_grid, -1, -1) == 0, \
            "Call to get_pixel_at(-1, -1) should have returned 0."

        assert get_pixel_at(test_grid, 2, 5) == 8,   \
            "Call to get_pixel_at(2, 5) should have returned 8."
        assert get_pixel_at(test_grid, 3, 5) == 0,   \
            "Call to get_pixel_at(3, 5) should have returned 0."
        assert get_pixel_at(test_grid, 2, 6) == 0,   \
            "Call to get_pixel_at(2, 6) should have returned 0."
        assert get_pixel_at(test_grid, 3, 6) == 0,   \
            "Call to get_pixel_at(3, 6) should have returned 0."

        assert get_pixel_at(test_grid, 1, 3) == 6,   \
            "Call to get_pixel_at(1, 3) should have returned 6."
    except AssertionError as e:
        # Print out a user-friendly error message
        print(e)


def average_of_surrounding(pixel_grid, i, j):
    """
    Returns the unweighted average of the values of the pixel at row i
    and column j and the eight pixels surrounding it.
    """
    pixel_sum = 0
    row = pixel_grid
    column = pixel_grid[0]
    # take values at (i+1, j+1), (i+1, j-1), (i-1, j-1), (i-1, j+1), (i+1, j),
    # (i-1, j), (i, j+1), (i, j-1)
    for row in (i-1, i, i+1):
        for column in (j-1, j, j+1):
            # sum those
            pixel_sum = get_pixel_at(pixel_grid, row, column) + pixel_sum
    # divide by 9
    return pixel_sum // 9


def test_average_of_surrounding():
    """ Basic, brief sanity checks for average_of_surrounding. """

    # Similarly to test_get_pixel_at, passing all of these tests
    # does not guarantee that your implementation of
    # average_of_surrounding is correct.

    test_grid = [
        [1, 2, 3, 4, 5, 6],
        [0, 2, 4, 6, 8, 10],
        [3, 4, 5, 6, 7, 8]
    ]

    try:
        assert average_of_surrounding(test_grid, 0, 0) == 0, \
            "average_of_surrounding(test_grid, 0, 0) should have returned 0."
        assert average_of_surrounding(test_grid, 2, 5) == 3, \
            "average_of_surrounding(test_grid, 2, 5) should have returned 3."
    except AssertionError as e:
        print(e)


def blur(pixel_grid):
    """
    Given pixel_grid (a grid of pixels), returns a new grid of pixels
    that is the result of blurring pixel_grid. In the output grid,
    each pixel is the average of that pixel and its eight neighbors in
    the input grid.
    """
    # initialize returned list
    blurry_grid = []
    row = pixel_grid
    column = pixel_grid[0]
    for row in range(len(pixel_grid)):
        int = []
        for column in range(len(pixel_grid[0])):
            # apply average_of_surrounding to each value
            new_val = average_of_surrounding(pixel_grid, row, column)
            # append average values into new list
            int.append(new_val)
        # put these values into a new list
        blurry_grid.append(int)
    return blurry_grid


################################################################
# The main program begins here.
#
# Step A: Process command line arguments & get input_file name.
#
# sys.argv is a list of the arguments to the program, including
# the name of the program being run. If you call:
#
#    python blur_image.py an_image.png
#
# then sys.argv will be ['blur_image.py', 'an_image.png']
#

print("Welcome to the CSE 160 Image Blurring program!")

# Run the tests. This method prints nothing if the tests
# pass. This method prints an error message for the first
# error it encounters.
test_get_pixel_at()
test_average_of_surrounding()

# Print how to use the program correctly if it appears that it has
# been used incorrectly (with the wrong number of arguments).
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "<input_file>")
    print("  <input_file> should be either ")
    print("    (a) a CSV-formatted text file")
    print("       (as generated by the write_grid function), or")
    print("    (b) a black-and-white image file")
    print("       (as generated by color_to_gray.py).")
    print()
    print("  Blurs the given input file and outputs the result as:")
    print("   <input_file>_blurry.png (an image) and")
    print("   <input_file>_blurry_grid.txt (a CSV-formatted text file).")
    sys.exit()

# Get the path to the file that the user wants to blur.
input_file = sys.argv[1]

# Step B: Determine what type the input_file is, read the file
# contents into a grid of pixels stored as a list of lists of integers

# Get the file extension and filename of the input file.
# Don't worry about the details of how these two lines work.
path_without_extension, extension = os.path.splitext(input_file)
input_filename = os.path.basename(path_without_extension)

# Either read the file in as an image or as a grid based
# on the file extension.
# Although we only accept a CSV-formatted file, we use the txt extension
if extension == ".txt":
    input_grid = read_grid(input_file)
else:
    input_grid = read_image(input_file)

    # read_image returns None in case of error--if that
    # happens, exit the program.
    if input_grid is None:
        exit()

# Step C: Generate the output file names

# Generate names for the output files based on the name of
# the input file.
out_image_filename = input_filename + '_blurry.png'
out_grid_filename = input_filename + '_blurry_grid.txt'

# Step D: Apply the blur algorithm

new_grid = blur(input_grid)

# Step E: Write the result to both output files

write_image(out_image_filename, new_grid)
write_grid(out_grid_filename, new_grid)


print("Program done")

###
# Collaboration
###

# Please write your collaboration statement below:
