##############################################################################################################
# Author: chinmayms
#
# user_profile: Class which defines the state of a given profile in our social network.
#
##############################################################################################################


class UserProfile:

    """
    Class Variables
    user_id: user id of the given profile
    purchases: list of tuples which consist of the purchase and its timestamp.
    friends: list of user_ids who are friends of the given profile.

    """

    # Constructor which defines user_id and empty friends and purchase list.
    def __init__(self, user_id):

        self.user_id = user_id
        self.purchases = []
        self.friends = []

    def get_last_t_purchases(self, num_of_purchases):

        """
        :param num_of_purchases: number of purchases to consider from the latest state. ('T')
        :return: list of last 'T' purchases.

        """

        total_purchase = []

        for purchase in self.purchases[-num_of_purchases:]:
            total_purchase.append(purchase[0])

        return total_purchase

    def get_friend_list(self):

        """
        Getter for friend list
        :return: list of friends for the given user_id

        """

        return self.friends

    def add_friend(self, friend_id):

        """
        Adds given user_id to friend list for current profile.
        :param friend_id: user_id of profile to be added as friend

        """

        self.friends.append(friend_id)

    def add_purchase(self, amount, timestamp):

        """
        Adds a purchase to purchase list with given amount and timestamp

        :param amount: amount for purchase to be added
        :param timestamp: timestamp of purchase made.

        """

        self.purchases.append((amount, timestamp))

    def remove_friend(self, friend_id):

        """
        Remove given user_id from friends list of current profile
        :param friend_id:

        """
        if friend_id in self.friends:
            self.friends.remove(friend_id)

    def get_user_id(self):

        """
        Getter for user_id of current profile.
        :return: returns user_id of current profile.
        """

        return self.user_id






