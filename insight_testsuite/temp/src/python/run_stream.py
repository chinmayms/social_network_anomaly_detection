##############################################################################################################
# Author: chinmayms
#
# run_stream: run social network system by calling methods from engine.py
#
##############################################################################################################

# Python imports
import sys

# Project imports
from src.python.engine import run_batch_log, run_stream_log

# Run initial transaction processing and obtain social network properties
user_data, user_list, NUMBER_OF_TRACKED_PURCHASES, DEGREE_OF_SOCIAL_NETWORK = run_batch_log(sys.argv[1])


# Run Stream processing by passing the social network properties obtained above.
run_stream_log(sys.argv[2], sys.argv[3], user_data, user_list, NUMBER_OF_TRACKED_PURCHASES, DEGREE_OF_SOCIAL_NETWORK)
