import fraud_detection as fd
import math


def test_ones_and_tens_digit_histogram():
    # Easy to calculate case: 5 numbers, clean percentages.
    actual = fd.ones_and_tens_digit_histogram([127, 426, 28, 9, 90])
    expected = [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.2]
    for i in range(len(actual)):
        assert math.isclose(actual[i], expected[i])

    # Obscure and hard (by hand) to calculate frequencies
    input = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89,
             144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    actual = fd.ones_and_tens_digit_histogram(input)
    expected = [0.21428571428571427, 0.14285714285714285, 0.047619047619047616,
                0.11904761904761904, 0.09523809523809523, 0.09523809523809523,
                0.023809523809523808, 0.09523809523809523, 0.11904761904761904,
                0.047619047619047616]
    for i in range(len(actual)):
        assert math.isclose(actual[i], expected[i])


def test_extract_election_votes():
    # import the file
    filename = 'election-iran-2009.csv'
    column_names = ['Ahmadinejad']
    # list of expected output
    expected = [1131111, 623946, 325911, 1799255, 199654, 299357, 3819495,
                359578, 285984, 2214801, 341104, 1303129, 444480, 295177,
                450269, 1758026, 498061, 422457, 315689, 1160446, 573568,
                253962, 515211, 998573, 677829, 1289257, 572988, 482990,
                765723, 337178]
    # actual output
    actual = fd.extract_election_votes(filename, column_names)
    # compare with assert statement
    assert sorted(expected) == sorted(actual), "extract votes test failed"

    print("extract votes test passed")


def test_mean_squared_error():
    # import test values
    numbers1 = [1, 7, 9]
    numbers2 = [5, 4, 20]
    # expected output
    expected = 48.6666667
    # actual output
    actual = fd.mean_squared_error(numbers1, numbers2)
    # compare with assert statement
    assert math.isclose(actual, expected), "mse test failed"

    print("mse test passed")


def main():
    test_ones_and_tens_digit_histogram()
    test_extract_election_votes()
    test_mean_squared_error()
    # call other test functions here


if __name__ == "__main__":
    main()
