import twitter
import time, random, logging
import json

class crawl_twitter:
	def __init__(self):
		self.consumer_key="nhvaSdfkzTa2QQmEWAbu9g"
		self.consumer_secret="Shi3XBkLwocYdfHbptEoLK3KbHDQ5MRYyA4Qq9jEW4"
		self.access_token_key="224897371-ZipzKRKDopJdNjSc3zkTJUwfKwHdigKCBpCqcY7A"
		self.access_token_secret="9eSEibVq6axdZKTjXB0Vc8qlALV0xLsEoCsUXFqpNU"
		
		#Constants
		self.MAX_FRIENDS_NODE_COUNT = 1000
		self.MAX_NODE_COUNT = 1

		#DataStructures
		self.all_node_set = set()
		self.current_node_list = []
		self.user_id_to_friends_id_dict = {}

		#IO
		self.logger_file = 'crawl_twitter.log'
		self.crawled_nodes_file = 'crawled_nodes_output'

	def run_main(self):
		self.initialize_logger()
		self.run()

	def initialize_logger(self):
		logging.basicConfig(filename=self.logger_file, level=logging.INFO)
		logging.info("Initialized logger")	

	def run(self):
		api = twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, access_token_key=self.access_token_key, access_token_secret=self.access_token_secret)
		self.get_friends_id(api)
	

	def get_friends_id(self, api):

		#Local Data Structures		
		users_id_list = []
		traversed_node_count = 0
		crawled_file = open(self.crawled_nodes_file, 'w')

		user_ids = api.GetFriendIDs(screen_name='iam_KarthikC')
		self.current_node_list.extend(user_ids)

		for uid in self.current_node_list:

			if uid in self.all_node_set:
				continue

			users_id_list = api.GetFriendIDs(user_id=uid)
			if len(users_id_list) > self.MAX_FRIENDS_NODE_COUNT:
				users_id_list = self.get_random_user_ids(users_id_list)
			self.current_node_list.extend(users_id_list)
			self.all_node_set.add(self.current_node_list.pop(0))
			time.sleep(60)
			self.user_id_to_friends_id_dict[uid] = users_id_list
			logging.info("user_id %s added", uid)
			
			#Clearing data structures
			users_id_list = []
			traversed_node_count += 1
			if traversed_node_count > self.MAX_NODE_COUNT:
				crawled_file.write(json.dumps(self.user_id_to_friends_id_dict))
				crawled_file.write('--------------------------------------------')
				break

	def get_random_user_ids(self, users_id_list):

		randomized_streamlined_user_id_list = []
		friends_count = len(users_id_list)		

		while 1:
			random_num = random.randint(0, friends_count)
			
			randomized_streamlined_user_id_list.append(users_id_list.pop(random_num))
			
			if len(randomized_streamlined_user_id_list) == self.MAX_FRIENDS_NODE_COUNT:
				break
			friends_count -= 1
		
		return randomized_streamlined_user_id_list


if __name__ == "__main__":
	ct_obj = crawl_twitter()
	ct_obj.run_main()
