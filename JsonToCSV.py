import json,csv,os

class ConvertJsonToCSV:

	def __init__(self):
		
		#Output
		self.output_dir = "output"


		#Filenames
		self.friends_info_file = os.path.join(self.output_dir,'crawled_nodes_output')   #Don't hard code the file names. 
		self.csv_file = os.path.join(self.output_dir, 'twitter_data_edge_list')

		#FileDescriptor
		self.friends_info_fd = open(self.friends_info_file, 'r')
		self.csv_fd = csv.writer(open(self.csv_file, 'wb+'))

	def run_main(self):
		self.run()

	def run(self):
		friends_info_data = self.friends_info_fd.read()
		self.friends_info_dict = json.loads(friends_info_data)

		for key, value in self.friends_info_dict.iteritems():
			for node in value:
				self.csv_fd.writerow([key, node])

if __name__ == "__main__":
	convert_obj = ConvertJsonToCSV()
	convert_obj.run_main()
