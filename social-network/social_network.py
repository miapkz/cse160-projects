# Name: Mia Pekez
# CSE 160
# Homework 5

import utils  # noqa: F401, do not remove if using a Mac
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter


###
#  Problem 1a
###

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()

    practice_graph.add_edge("A", "B")
    practice_graph.add_edge("A", "C")
    practice_graph.add_edge("B", "C")
    practice_graph.add_edge("C", "D")
    practice_graph.add_edge("B", "D")
    practice_graph.add_edge("C", "F")
    practice_graph.add_edge("F", "D")
    practice_graph.add_edge("E", "D")

    return practice_graph


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


###
#  Problem 1b
###

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()
    rj.add_edges_from([("Nurse", "Juliet"), ("Juliet", "Capulet"),
                       ("Capulet", "Paris")])
    rj.add_edges_from([("Juliet", "Tybalt"), ("Capulet", "Tybalt")])
    rj.add_edges_from([("Juliet", "Romeo"), ("Juliet", "Friar Laurence")])
    rj.add_edges_from([("Romeo", "Friar Laurence"), ("Romeo", "Mercutio"),
                       ("Romeo", "Montague"), ("Romeo", "Benvolio")])
    rj.add_edges_from([("Benvolio", "Montague"), ("Montague", "Escalus")])
    rj.add_edges_from([("Capulet", "Escalus"), ("Capulet", "Paris")])
    rj.add_edges_from([("Mercutio", "Escalus"), ("Mercutio", "Paris")])
    rj.add_edges_from([("Escalus", "Paris")])

    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


###
#  Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    # This function has already been implemented for you.
    # You do not need to add any more code to this (short!) function.
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    # empty set for friends of friends
    fr_of_fr_set = set()
    # for each friend of user, add their friends to set
    for n in graph.neighbors(user):
        fr_of_fr_set = fr_of_fr_set | set(graph.neighbors(n))
        # remove the original friend and immediate friends
    return fr_of_fr_set - set([user]) - friends(graph, user)


def common_friends(graph, user1, user2):
    """Finds and returns the set of friends that user1 and user2 have in
    common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    # take intersection of neighbors of user 1 and user 2
    com_friends_set = set(graph.neighbors(user1)) & set(graph.neighbors(user2))
    return com_friends_set


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      number_of_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    # create empty dictionary
    n_of_com_fr = {}
    fr_of_fr = friends_of_friends(graph, user)
    # for each user, run through neighbors of their neighbors
    for fr in fr_of_fr:
        # implement common_friends with user and fr
        # length of com_friends_set is number of common friends
        num = len(common_friends(graph, user, fr))
        # map to dictionary
        n_of_com_fr[fr] = num
    return n_of_com_fr


def number_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    # initialize final list and dict to tuple list
    s_list = []
    dict_to_tuple = []
    # turn the input dictionary into a list of tuples
    for key, val in map_with_number_vals.items():
        t = tuple([key, val])
        dict_to_tuple.append(t)
    # sort alphabetically
    alpha_sort = sorted(dict_to_tuple, key=itemgetter(0))
    # sort by number value
    sorted_list = sorted(alpha_sort, key=itemgetter(1), reverse=True)
    # return corresponding keys in a list
    for i in sorted_list:
        s_list.append(i[0])
    return s_list


def rec_number_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    # initalize final list
    final_rec = []
    # find how many common friends
    unsorted_lst = number_of_common_friends_map(graph, user)
    # turn returned dictionary into a list of tuples
    dict_to_tuple = []
    for key, val in unsorted_lst.items():
        t = tuple([key, val])
        dict_to_tuple.append(t)
    # sort alphabetically
    alpha_sort = sorted(dict_to_tuple, key=itemgetter(0))
    # sort by number of common friends
    sorted_lst = sorted(alpha_sort, key=itemgetter(1), reverse=True)
    # return just keys aka names of common friends
    for i in sorted_lst:
        final_rec.append(i[0])
    return final_rec


###
#  Problem 3
###

def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    # initialize final list
    influence_dict = {}
    # go through each common friend
    for friend in number_of_common_friends_map(graph, user):
        ind_score = 0
        for person in common_friends(graph, user, friend):
            # how many other friends each friend has
            fr_of_fr = len(friends(graph, person))
            # add up the scores
            ind_score = ind_score + 1/fr_of_fr
        influence_dict[friend] = ind_score
    return influence_dict


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    # initalize final list
    final_rec_by_inf = []
    # find influence scores for each friend
    unsorted_lst = influence_map(graph, user)
    # turn returned dictionary into a list of tuples
    dict_to_tuple = []
    for key, val in unsorted_lst.items():
        t = tuple([key, val])
        dict_to_tuple.append(t)
    # sort alphabetically
    alpha_sort = sorted(dict_to_tuple, key=itemgetter(0))
    # sort by number of common friends
    sorted_lst = sorted(alpha_sort, key=itemgetter(1), reverse=True)
    # return just keys aka names of common friends
    for i in sorted_lst:
        final_rec_by_inf.append(i[0])
    return final_rec_by_inf


###
#  Problem 5
###

def get_facebook_graph():
    """Builds and returns the facebook graph
    """
    facebook = nx.Graph()
    # open file to be read
    facebook_file = open("facebook-links-small.txt")
    # go thru every line in facebook file
    for line_of_text in facebook_file:
        users = line_of_text.split()
        # remove the third item(timestamp)
        users.pop(2)
        # convert strings into ints
        users_as_int = [int(x) for x in users]
        # print(users_as_int)
        facebook.add_edge(users_as_int[0], users_as_int[1])
    return facebook

# def draw_facebook(graph):
    """Draw the rj graph to the screen and to a file.
    """
    # nx.draw_networkx(graph)
    plt.savefig("facebook.pdf")
    plt.show()


def main():
    # practice_graph = get_practice_graph()
    # Comment out this line after you have visually verified your practice
    # graph.
    # Otherwise, the picture will pop up every time that you run your program.
    # draw_practice_graph(practice_graph)

    rj = get_romeo_and_juliet_graph()
    # Comment out this line after you have visually verified your rj graph and
    # created your PDF file.
    # Otherwise, the picture will pop up every time that you run your program.
    # draw_rj(rj)

    ###
    #  Problem 4
    ###

    unchanged = []
    changed = []
    for person in rj:
        if (rec_number_common_friends(rj, person) == recommend_by_influence
                (rj, person)):
            unchanged.append(person)
            unchanged_sorted = sorted(unchanged)
        else:
            changed.append(person)
            changed_sorted = sorted(changed)

    print("Problem 4:")
    print("Unchanged Recommendations:", unchanged_sorted)
    print("Changed Recommendations:", changed_sorted)

    ###
    #  Problem 5
    ###
    facebook = get_facebook_graph()

    # draw_facebook(facebook)

    # assert len(facebook.nodes()) == 63731
    # assert len(facebook.edges()) == 817090

    ###
    #  Problem 6
    ###
    print("Problem 6:")
    for user in sorted(facebook.nodes):
        # if user is multiple of 1000
        if user % 1000 == 0:
            # apply rec_number_common_friends
            rec = rec_number_common_friends(facebook, user)
            # print first 10 items in returned list
            rec_10 = rec[0:10]
            print(user, "(by number_of_common_friends):", rec_10)

    ###
    #  Problem 7
    ###
    print("Problem 7:")
    for user in sorted(facebook.nodes):
        # if user is multiple of 1000
        if user % 1000 == 0:
            # apply recommend_by_influence
            inf = recommend_by_influence(facebook, user)
            # print first 10 items in returned list
            inf_10 = inf[0:10]
            print(user, "(by influence):", inf_10)

    ###
    #  Problem 8
    ###
    print("Problem 8:")

    # initialize a list for same and a list for different
    num_same_rec = []
    num_diff_rec = []
    # loop thru all the users in facebook graph
    for user in facebook.nodes:
        # if user is a multiple of 1000
        if user % 1000 == 0:
            rec = rec_number_common_friends(facebook, user)
            inf = recommend_by_influence(facebook, user)
            # if rec from num of common friends and rec by influence are equal
            if inf == rec:
                # add user to list of same
                num_same_rec.append(user)
            else:
                # if two recs different add user to list of different
                num_diff_rec.append(user)
    # print the length of both lists
    print("Same:", len(num_same_rec))
    print("Different:", len(num_diff_rec))


if __name__ == "__main__":
    main()


###
#  Collaboration
###

# Please write your collaboration statement below:
