import twitter
import time, random, logging
import json
import os, codecs

class crawl_twitter:
	def __init__(self):

		#Security Credentials
		self.consumer_key="nhvaSdfkzTa2QQmEWAbu9g"
		self.consumer_secret="Shi3XBkLwocYdfHbptEoLK3KbHDQ5MRYyA4Qq9jEW4"
		self.access_token_key="224897371-ZipzKRKDopJdNjSc3zkTJUwfKwHdigKCBpCqcY7A"
		self.access_token_secret="9eSEibVq6axdZKTjXB0Vc8qlALV0xLsEoCsUXFqpNU"
		
		#Constants
		self.MAX_FRIENDS_NODE_COUNT = 1000
		self.MAX_NODE_COUNT = 300
		self.MY_SCREEN_NAME = 'iam_KarthikC'
		self.MAX_NODE_TO_DUMP = 30
		self.SLEEP_TIME = 120

		#DataStructures
		self.all_node_set = set()
		self.current_node_list = []
		self.user_id_to_friends_id_dict = {}

		#IOFiles
		self.logger_file = os.path.join('OUTPUT','crawl_twitter.log')

	def run_main(self):
		self.initialize_logger()
		self.run()

	def initialize_logger(self):
		logging.basicConfig(filename=self.logger_file, level=logging.INFO)
		logging.info("Initialized logger")	

	def run(self):
		#Create API Object
		api = twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, access_token_key=self.access_token_key, access_token_secret=self.access_token_secret)
		
		# After every api call, sleep for one min
		time.sleep(self.SLEEP_TIME) 
		logging.info("Sleeping after sleep 1")
		
		#GetFriendsIds
		self.get_friends_id(api)
	

	def get_friends_id(self, api):
		#Crawl a node and its friends' ids and dump in a file

		#Local Data Structures		
		users_id_list = []

		#Local variables
		traversed_node_count = 0
		max_dump_count = 0
		dump_count =0

		#Starting the crawling from my twitter acc/ Me as the center node
		user_ids = api.GetFriendIDs(screen_name=self.MY_SCREEN_NAME)
		time.sleep(self.SLEEP_TIME)
		logging.info("Sleeping after sleep 2")
		self.current_node_list.extend(user_ids)

		#Now employ BFS to all other friend's node
		for uid in self.current_node_list:

			#If this node is already seen, continue . 
			if uid in self.all_node_set:
				continue
			users_id_list = api.GetFriendIDs(user_id=uid)
			time.sleep(self.SLEEP_TIME)
			logging.info("Sleeping after sleep 3")

			#If any node has friends more than max friends count, then select randomly a 1000 nodes from them.
			if len(users_id_list) > self.MAX_FRIENDS_NODE_COUNT:
				users_id_list = self.get_random_user_ids(users_id_list)
			self.current_node_list.extend(users_id_list)
			self.all_node_set.add(self.current_node_list.pop(0))


			#Only one api call is allowed per two min. So sleep for every two min after every call
			self.user_id_to_friends_id_dict[uid] = users_id_list

			#Clearing data structures
			users_id_list = []
		
			traversed_node_count += 1
			max_dump_count += 1			

			#If max nodes are crawled then stop crawling
			if traversed_node_count > self.MAX_NODE_COUNT:
				break
			
			logging.info("user_id %s added and its count is %s" % (uid, traversed_node_count))


			#Write a node and its friends' ids in a file after some nodes are crawled
			if max_dump_count == self.MAX_NODE_TO_DUMP:

				#FileOperations
				self.crawled_nodes_file = os.path.join('OUTPUT','crawled_nodes_output%s' % (dump_count))
				crawled_file = codecs.open(self.crawled_nodes_file, 'w', 'utf-8')

				#FileDump
				crawled_file.write(json.dumps(self.user_id_to_friends_id_dict))
	
				#DS Operations
				dump_count += 1
				max_dump_count = 0
				self.user_id_to_friends_id_dict = {}

				#Closing file descriptor
				crawled_file.close()


	def get_random_user_ids(self, users_id_list):
		#Return random subset of nodes from the given big list of nodes
		
		#Local ds
		randomized_streamlined_user_id_list = []

		#Local variables
		friends_count = len(users_id_list)		

		while 1:
			random_num = random.randint(0, friends_count)
			
			randomized_streamlined_user_id_list.append(users_id_list.pop(random_num))
			
			if len(randomized_streamlined_user_id_list) > self.MAX_FRIENDS_NODE_COUNT:
				break
			friends_count -= 1
		
		return randomized_streamlined_user_id_list


if __name__ == "__main__":
	ct_obj = crawl_twitter()
	ct_obj.run_main()
