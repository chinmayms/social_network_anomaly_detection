##############################################################################################################
# Author: chinmayms
#
# unit_tests: Run unit tests on user_profile class methods to check whether they maintain consistent state
#             and check whether all transactions are atomic
#
##############################################################################################################

# Python imports
import os
import random
from dateutil import parser

# Project imports
from src.python.user_profile import UserProfile
from src.python.engine import run_stream_log,run_batch_log


class TestSuite:

    # Check if constructor values are getting assigned correctly
    def test_default_constructor_values(self):

        user_id = random.randint(1, 101)
        profile = UserProfile(user_id)

        assert profile.user_id == user_id
        assert isinstance(profile.friends,list)
        assert isinstance(profile.purchases,list)

    # Test add friend functionality
    def test_add_friend_functionality(self):

        user_id = random.randint(1, 10)
        profile = UserProfile(user_id)

        initial_length = len(profile.get_friend_list())

        friend = random.randint(11,20)

        profile.add_friend(friend)

        assert friend in profile.get_friend_list()
        assert len(profile.get_friend_list()) > initial_length

    # Test Add Purchase functionality
    def test_add_purchase(self):

        user_id = random.randint(1,100)
        profile = UserProfile(user_id)

        date_str = "2017-06-13 11:33:01"

        last_t_purchases = random.randint(1,10)
        initial_purchases = profile.get_last_t_purchases(last_t_purchases)
        initial_length = len(profile.purchases)
        amount = float(random.randint(1000,2000))
        profile.add_purchase(amount, date_str)

        assert isinstance(profile.purchases[0],tuple)
        assert (amount, str(parser.parse(date_str))) in profile.purchases
        assert initial_purchases != profile.get_last_t_purchases(last_t_purchases)
        assert len(profile.purchases) > initial_length

    # Test getting last 'T' purchases functionality with regression values
    def test_get_lst_t_purchases(self):

        user_id = random.randint(1, 100)
        profile = UserProfile(user_id)

        date_str = "2017-06-13 11:33:01"
        amount = float(random.randint(1000, 2000))
        profile.add_purchase(amount, date_str)

        last_t_purchases = random.randint(1000, 2000)

        assert isinstance(profile.get_last_t_purchases(last_t_purchases),list)
        assert len(profile.get_last_t_purchases(last_t_purchases)) <= last_t_purchases

    # Test remove friend functionality and check for edge cases
    def test_remove_friend(self):

        user_id = random.randint(1, 10)
        profile = UserProfile(user_id)

        initial_length = len(profile.get_friend_list())

        friend = random.randint(11, 20)

        profile.add_friend(friend)

        intermediate_length = len(profile.get_friend_list())

        assert friend in profile.get_friend_list()
        assert intermediate_length > initial_length

        profile.remove_friend(friend)

        final_length = len(profile.get_friend_list())

        assert friend not in profile.get_friend_list()
        assert final_length < intermediate_length

        # Try removing friend which does not exist in friend list
        profile.remove_friend(random.randint(1000,2000))

        assert final_length == len(profile.get_friend_list())

    # Test initial batch log processing
    def test_run_batch_log(self):

        user_data, user_list, NUMBER_OF_TRACKED_PURCHASES,\
                              DEGREE_OF_SOCIAL_NETWORK = run_batch_log("../log_input/batch_log.json")

        assert isinstance(user_data,dict)
        assert isinstance(user_list,set)
        assert isinstance(NUMBER_OF_TRACKED_PURCHASES,int)
        assert isinstance(DEGREE_OF_SOCIAL_NETWORK,int)
        assert NUMBER_OF_TRACKED_PURCHASES >= 0
        assert DEGREE_OF_SOCIAL_NETWORK > 0

    # Test Streaming and creation of output file
    def test_run_stream_log(self):

        # Run initial batch log file processing
        user_data, user_list, NUMBER_OF_TRACKED_PURCHASES,\
        DEGREE_OF_SOCIAL_NETWORK = run_batch_log("../log_input/batch_log.json")

        # Provide streaming and output file paths
        stream_log_file_path = "../log_input/stream_log.json"
        output_file_path = "../log_output/flagged_purchases.json"

        # Remove any existing output files , if any
        os.remove(output_file_path)

        run_stream_log(stream_log_file_path,output_file_path,user_data,user_list,
                       NUMBER_OF_TRACKED_PURCHASES,DEGREE_OF_SOCIAL_NETWORK)

        # Check if output file got created
        assert os.path.isfile(output_file_path)












