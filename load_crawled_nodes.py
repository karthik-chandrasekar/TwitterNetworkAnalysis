import json

class CrawledInput:
	def __init__(self):
	
		#Filenames
		self.friends_info_file = 'crawled_nodes_output'
		
		#FileDescriptor
		self.friends_info_fd = open(self.friends_info_file, 'r')

	def run(self):
		friends_info_data = self.friends_info_fd.read()
		import pdb;pdb.set_trace()
		friends_info_dict = json.loads(friends_info_data)	

if __name__ == "__main__":
	ci  = CrawledInput()
	ci.run()
