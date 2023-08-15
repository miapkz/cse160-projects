import utils  # noqa: F401, do not remove if using a Mac
# add your imports BELOW this line
import csv
import matplotlib.pyplot as plt
import random


def ones_and_tens_digit_histogram(numbers):
    '''
    Input:
        a list of numbers.
    Returns:
        a list where the value at index i is the frequency in which digit i
        appeared in the ones place OR the tens place in the input list. This
        returned list will always have 10 numbers (representing the frequency
        of digits 0 - 9).

    For example, given the input list
        [127, 426, 28, 9, 90]
    This function will return
        [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.2]

    That is, the digit 0 occurred in 20% of the one and tens places; 2 in 30%
    of them; 6, 7, and 8 each in 10% of the ones and tens, and 9 occurred in
    20% of the ones and tens.

    See fraud_detection_tests.py for additional cases.
    '''
    histogram = [0] * 10

    # first fill histogram with counts
    for i in numbers:
        # 1's place
        histogram[i % 10] += 1

        # 10's place
        histogram[i // 10 % 10] += 1

    # normalize over total counts
    for i in range(len(histogram)):
        histogram[i] /= len(numbers) * 2

    return histogram

# Your Set of Functions for this assignment goes in here


def extract_election_votes(filename, column_names):
    '''
    Input:
        filename and a list of column names.
    Returns:
        a list of integers that contains the values in those columns from
        every row (the order of the integers does not matter).
    '''
    # initiate empty list
    list = []
    # open and read file
    file = open(filename)
    reader = csv.DictReader(file)
    for row in reader:
        for column_name in column_names:
            # remove commas from input values
            vote = row[column_name].replace(",", "")
            # append values and turn into ints
            list.append(int(vote))
    file.close()
    return list


def plot_iran_least_digits_histogram(histogram):
    '''
    Input:
        a histogram (as created by ones_and_tens_digit_histogram).
    Returns:
        Creates and saves a graph of the frequencies of the ones and tens
        digits for the Iranian election data to a file named iran-digits.png.
        Returns nothing.
    '''
    # digit value is x axis, frequency is y axis
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # blue line = y is 0.1
    y1 = []
    for i in range(1, 11):
        y1.append(0.1)
    # orange line = values extracted from csv
    votes = extract_election_votes('election-iran-2009.csv',
                                   ["Ahmadinejad", "Rezai", "Karrubi",
                                    "Mousavi"])
    y = ones_and_tens_digit_histogram(votes)
    plt.plot(x, y, color='orange', label="iran")
    plt.plot(x, y1, color='blue', label="ideal")
    plt.title("Distribution of the last two digits in Iranian dataset")
    plt.legend(loc='upper left')
    plt.xlabel("Digit")
    plt.ylabel("Frequency")
    plt.savefig("iran-digits.png")
    # plt.show()


def random_sample_generator(n):
    '''
    Input:
        An integer.
    Returns:
        A list of size n that is a collection of random numbers 0 <= x < 100.
    '''
    lst = []
    for i in range(n+1):
        lst.append(random.randint(0, 100))
    return lst


def plot_dist_by_sample_size():
    '''
    Creates and saves one graph of five different collections (sizes 10, 50,
    100, 1000 and 10,000) of random numbers where every element in the
    collection is a different random number x such that 0 <= x < 100.
    '''
    # create x axis
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # create the ideal line at y=0.1
    y1 = []
    for i in range(1, 11):
        y1.append(0.1)
    # obtain the five samples of different sizes using helper function
    for n in [10, 50, 100, 1000, 10000]:
        sample = random_sample_generator(n)
        # plot the random samples using histogram function
        input = ones_and_tens_digit_histogram(sample)
        plt.plot(x, input, label=(str(n) + " random samples"))
    # # make title and legend and save the graph
    plt.title("Distribution of the last two digits in randomly generated"
              " samples")
    plt.legend(loc='upper left')
    plt.savefig("random-digits.png")
    # plt.show()


def mean_squared_error(numbers1, numbers2):
    '''
    Input:
        Two lists of numbers.
    Returns:
        The mean squared error between the lists. For each point in one
        dataset, compute the difference between it and the corresponding
        point in the other dataset and then square the difference.
        Take the average of these squared differences.

    '''
    # initialize sum of squared differences
    sum = 0
    # for each item in list, difference between it and corresponding item
    for i in range(len(numbers1)):
        diff = (numbers1[i] - numbers2[i])
        # square the difference
        diff_sq = diff**2
        # add up all the squared differences
        sum = sum + diff_sq
        # average the sum
        avg = sum/(len(numbers1))
    return avg


def calculate_mse_with_uniform(histogram):
    '''
    Input:
        A histogram (a list of frequencies).
    Returns:
        The mean squared error between the given histogram and the uniform
        distribution.
    '''
    # histogram output is list
    # ideal distribution is always 0.1
    uniform_dist = []
    for i in range(len(histogram)):
        uniform_dist.append(0.1)
    # mean squared error between those two
    mse = mean_squared_error(uniform_dist, histogram)
    return mse


def compare_iran_mse_to_samples(iran_mse, number_of_iran_datapoints):
    '''
    Inputs:
        Iranian MSE (as computed by calculate_mse_with_uniform()) and the
        number of data points in the Iranian dataset.
    Returns:
        Number of MSE's from a random sample of 10,000 that are larger than or
        equal to the Iran MSE.
        Number of MSE's from a random sample of 10,000 that are smaller than
        the Iran MSE.
        The Iranian election null hypothesis rejection level.
    Random sample of 10,000 is generated such that 0 <= x < 100 and each group
    is the same size as the Iranian election data.
    '''
    # obtain number of iran datapoints
    datapoints = len((extract_election_votes('election-iran-2009.csv',
                                             ["Ahmadinejad", "Rezai",
                                              "Karrubi", "Mousavi"])))
    # set iranian mse into a variable
    iran_mse = calculate_mse_with_uniform(ones_and_tens_digit_histogram
                                          (extract_election_votes
                                           ('election-iran-2009.csv',
                                            ["Ahmadinejad", "Rezai",
                                             "Karrubi", "Mousavi"])))
    print("2009 Iranian election MSE:", iran_mse)
    more_than = 0
    less_than = 0
    # generate random samples
    for i in range(10000):
        sample = random_sample_generator(datapoints)
        # plot the samples as histogram
        input = ones_and_tens_digit_histogram(sample)
        # calculate their mse
        sample_mse = calculate_mse_with_uniform(input)
        # if random sample mse>=iran mse, keep count
        if sample_mse >= iran_mse:
            more_than += 1
        # if random sample mse<iran mse, keep count
        else:
            less_than += 1
    print("Quantity of MSEs larger than or equal to the 2009 Iranian election"
          " MSE:", more_than)
    print("Quantity of MSEs smaller than the 2009 Iranian election"
          " MSE:", less_than)
    print("2009 Iranian election null hypothesis rejection level p:",
          more_than/10000)

# The code in this function is executed when this
# file is run as a Python program


def main():
    # Code that calls functions you have written above
    # e.g. extract_election_vote_counts() etc.
    # This code should produce the output expected from your program.
    extract_election_votes("election-iran-2009.csv", ["Ahmadinejad", "Rezai",
                                                      "Karrubi", "Mousavi"])
    plot_iran_least_digits_histogram(ones_and_tens_digit_histogram)
    plot_dist_by_sample_size()
    mean_squared_error([1, 4, 9], [6, 5, 4])
    calculate_mse_with_uniform(ones_and_tens_digit_histogram
                               (extract_election_votes
                                ('election-iran-2009.csv',
                                 ["Ahmadinejad", "Rezai",
                                  "Karrubi", "Mousavi"])))
    compare_iran_mse_to_samples(calculate_mse_with_uniform
                                (ones_and_tens_digit_histogram
                                 (extract_election_votes
                                  ('election-iran-2009.csv',
                                   ["Ahmadinejad", "Rezai",
                                    "Karrubi", "Mousavi"]))),
                                len((extract_election_votes
                                     ('election-iran-2009.csv',
                                      ["Ahmadinejad", "Rezai",
                                       "Karrubi", "Mousavi"]))))


if __name__ == "__main__":
    main()
