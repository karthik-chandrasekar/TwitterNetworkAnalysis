import os,json
from crawl_twitter import crawl_twitter


class PartialCrawlTwitter(crawl_twitter):
	def __init__(self):
		crawl_twitter.__init__(self)

		#Filenames
		self.friends_info_file = 'crawled_nodes_output'   #Don't hard code the file names. 
		
		#FileDescriptor
		self.friends_info_fd = open(self.friends_info_file, 'r')

		#DataStructures
		self.crawled_nodes_set = set()

		#GlobalVariables
		self.MY_SCREEN_NAME = 'ambikaiyer29'
		self.MAX_NODE_COUNT = 500
		self.MAX_NODE_TO_DUMP = 100



	def run_main_mod(self):
		friends_info_data = self.friends_info_fd.read()
		self.friends_info_dict = json.loads(friends_info_data)

		#Crawled nodes set
		self.get_crawled_nodes_set()

		#Populate the already crawled nodes set
		self.all_followers_node_set = self.all_followers_node_set.union(self.crawled_nodes_set)


		self.run()


	def get_crawled_nodes_set(self):
		for key, value in self.friends_info_dict.iteritems():
			self.crawled_nodes_set.add(key)

		print "Crawled nodes set length %s"  % len(self.crawled_nodes_set)


if __name__ == "__main__":
	crawl_obj = PartialCrawlTwitter()
	crawl_obj.run_main_mod()
