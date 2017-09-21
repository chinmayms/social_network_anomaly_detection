##########################################################################
# Author: chinmayms
#
# engine: The core engine which streams through all files and updates the data structures
#         and output file to maintain data and state of the social network.
#
##########################################################################

# Python imports
import json
import numpy as np
from dateutil import parser
from collections import OrderedDict

# Project imports
from src.python.user_profile import UserProfile


def check_profile_existence(user_list, user_id):
    """Checks if the given user_id is already part of the system.

    :param user_list: Set which contains list of user_ids which are part of the system.
    :param user_id: Data Structure (Dictionary) which stores all user data objects.

    :return: boolean value signifying whether record for given user_id already exists in system."""

    if user_id in user_list:
        return True

    return False


def add_user(user_list, user_data, user_id):
    """Adds a given user to both user_list and user_data data structure by creating a new user object.

    :param user_list: Set which contains list of user_ids which are part of the system.
    :param user_data: Data Structure (Dictionary) which stores all user data objects.
    :param user_id: user_id to be added."""

    user_list.add(user_id)
    user_data[user_id] = UserProfile(user_id)


def run_batch_log(input_file_path):
    """Runs processing using batch_log.json file transactions to create initial social network state.

    :param input_file_path: Input file path to read initial batch_log.json file to create initial state.

    :return user_data: Dictionary which maps user_ids to their profile objects which contain profile data and state.
    :return user_list: Set which contains all user_ids part of the system."""

    # Declare user_list and user_data data structures.

    # user_list contains all user_ids part of the system
    user_list = set()

    # user_data maps user_ids to their associated profile objects
    user_data = dict()

    try:
        input_file = open(input_file_path, 'r')
    except:
        raise TypeError("Provide valid input file path")

    params = json.loads(input_file.readline())

    # Read 'D' and 'T' params from file and store them in cnstant variables.
    DEGREE_OF_SOCIAL_NETWORK = int(params['D'])
    NUMBER_OF_TRACKED_PURCHASES = int(params['T'])

    # Create initial state from remaining lines of batch_log.json
    for event in input_file.readlines():

        event_details = json.loads(event)

        event_type = event_details['event_type']

        # Purchase events
        if event_type == 'purchase':
            user_id = int(event_details['id'])

            # If user profile for given user_id already exists, add purchase to
            # its object.
            if check_profile_existence(user_list, user_id):
                user_data[user_id].add_purchase(float(event_details['amount']),
                                                parser.parse(event_details['timestamp']))
            # If user profile does not exist, create new user profile and add
            # purchase to its object.
            else:
                add_user(user_list,user_data,user_id)
                user_data[user_id].add_purchase(float(event_details['amount']),
                                                parser.parse(event_details['timestamp']))
        # Friend Add Event
        elif event_type == 'befriend':
            user_id_1 = int(event_details['id1'])
            user_id_2 = int(event_details['id2'])

            # Check if both accounts exist
            account_1_exists = check_profile_existence(user_list, user_id_1)
            account_2_exists = check_profile_existence(user_list, user_id_2)

            # If either/one accounts do not exist, create new user profile
            if not account_1_exists:
                add_user(user_list,user_data, user_id_1)
            if not account_2_exists:
                add_user(user_list,user_data, user_id_2)

            # Check if two users are already friends, if not, add them to each
            # other's friend lists
            if user_id_2 not in user_data[user_id_1].get_friend_list():
                user_data[user_id_1].add_friend(user_id_2)
            if user_id_1 not in user_data[user_id_2].get_friend_list():
                user_data[user_id_2].add_friend(user_id_1)

        # Remove Friend Event
        elif event_type == 'unfriend':

            user_id_1 = int(event_details['id1'])
            user_id_2 = int(event_details['id2'])

            # Remove each other from respective friend lists

            # Existence of user_id in friend_list check is done at class level
            # implementation of remove_friend method
            user_data[user_id_1].remove_friend(user_id_2)
            user_data[user_id_2].remove_friend(user_id_1)

    return user_data, user_list, NUMBER_OF_TRACKED_PURCHASES, DEGREE_OF_SOCIAL_NETWORK


def run_stream_log(stream_log_file_path, output_file_path, user_data, user_list, NUMBER_OF_TRACKED_PURCHASES, DEGREE_OF_SOCIAL_NETWORK):
    """Run stream processing using stream_log.json file transactions to determine flagged purchases.

    :param stream_log_file_path: file_path to read stream_log.json.
    :param output_file_path: path to write flagged_purchases.json.
    :param user_data: Dictionary which maps user_ids to their profile objects which contain profile data and state.
    :param user_list: Set which contains all user_ids part of the system.
    :param NUMBER_OF_TRACKED_PURCHASES: Threshold for previous transaction consideration.
    :param DEGREE_OF_SOCIAL_NETWORK: Degree of social network to consider while flagging purchases."""

    # Read stream_log.json file
    try:
        stream_file = open(stream_log_file_path, 'r')
    except:
        raise TypeError("Please provide valid file path")

    # Create flagged_purchases.json file using given file path.
    try:
        flagged_file = open(output_file_path, 'w')
    except:
        raise TypeError("Please provide valid file path")

    # Stream every transaction in the file
    for event in stream_file.readlines():

        event_details = json.loads(event)

        event_type = event_details['event_type']

        # Purchase events
        if event_details['event_type'] == 'purchase':
            user_id = int(event_details['id'])

            # If user profile for given user_id already exists, add purchase to
            # its object.
            if check_profile_existence(user_list, user_id):
                user_data[user_id].add_purchase(float(event_details['amount']),
                                                parser.parse(event_details['timestamp']))

            # If user profile does not exist, create new user profile and add
            # purchase to its object.
            else:
                add_user(user_list,user_data,user_id)
                user_data[user_id].add_purchase(float(event_details['amount']),
                                                parser.parse(event_details['timestamp']))

            # Get friend list for given user_id
            friends_list = user_data[user_id].get_friend_list()

            """Intermediate set to nest through degree of social network.
            We use sets to avoid duplication of friends as we iterate through a graph of friends."""

            intermediate_list = set(friends_list)

            # total_list will be a set which encapsulates entire network withing
            # the given degree
            total_list = set()

            # Add friends at degree '0' (direct friends) to total_list
            total_list = total_list.union(intermediate_list)

            # Declare initial depth to zero.
            depth = 0

            # Iterate through network and add friends until given degree is
            # attained.
            while depth < DEGREE_OF_SOCIAL_NETWORK - 1:
                temp_set = set()
                for friend in intermediate_list:
                    total_list = total_list.union(set(user_data[friend].get_friend_list()))
                    temp_set = temp_set.union(set(user_data[friend].get_friend_list()))
                intermediate_list = temp_set
                depth += 1

            """Because of the graph, it may be possible that the user_id itself might have gotten added to the list,
            if that is the case, we remove it."""
            if user_id in total_list:
                total_list.remove(user_id)

            # contains last 'T' transactions from found network of degree 'D'
            # for given purchase of the given user_id.
            total_spend = []

            # Add transaction to total_spend by iterating over list of friends
            # within degree 'D'
            for every_connect_friend in total_list:
                total_spend += user_data[every_connect_friend].get_last_t_purchases(NUMBER_OF_TRACKED_PURCHASES)

            # Find mean of all found purchases
            mean = np.mean(np.array(total_spend))

            # Find standard deviation of all found purchases
            std = np.std(np.array(total_spend))

            # Check if current purchase is at least 3 standard deviations above
            # mean of list of purchases
            if float(event_details['amount']) > mean + 3 * std:

                # If purchase > mean + 3 * std, create ordered dict to preserve
                # order of keys and add all details to it.
                flagged_details = OrderedDict()
                flagged_details['event_type'] = event_details['event_type']
                flagged_details['timestamp'] = event_details['timestamp']
                flagged_details['id'] = event_details['id']
                flagged_details['amount'] = event_details['amount']
                flagged_details['mean'] = '{:.2f}'.format(int(mean * 10**2) / 10.0**2)
                flagged_details['sd'] = '{:.2f}'.format(int(std * 10**2) / 10.0**2)
                flagged_file.write(json.dumps(flagged_details) + "\n")

        # Friend Add Event
        elif event_type == 'befriend':

            user_id_1 = int(event_details['id1'])
            user_id_2 = int(event_details['id2'])

            # Check if both accounts exist
            account_1_exists = check_profile_existence(user_list, user_id_1)
            account_2_exists = check_profile_existence(user_list, user_id_2)

            # If either/one accounts do not exist, create new user profile
            if not account_1_exists:
                add_user(user_list, user_data, user_id_1)
            if not account_2_exists:
                add_user(user_list, user_data, user_id_2)

            # Check if two users are already friends, if not, add them to each
            # other's friend lists
            if user_id_2 not in user_data[user_id_1].get_friend_list():
                user_data[user_id_1].add_friend(user_id_2)
            if user_id_1 not in user_data[user_id_2].get_friend_list():
                user_data[user_id_2].add_friend(user_id_1)

        # Friend Remove Event
        elif event_type == 'unfriend':

            user_id_1 = int(event_details['id1'])
            user_id_2 = int(event_details['id2'])

            # Remove each other from respective friend lists
            user_data[user_id_1].remove_friend(user_id_2)
            user_data[user_id_2].remove_friend(user_id_1)

    # Close file opened for writing.
    flagged_file.close()
