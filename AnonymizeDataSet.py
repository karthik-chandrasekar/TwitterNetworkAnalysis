import json, codecs, os

class AnonymizeData:
	def __init__(self):
		
		#Directories list
		self.output_dir = 'output'

		#Filenames
		self.friends_info_file = os.path.join(self.output_dir,'crawled_nodes_output')
		self.twitter_data_userid_hash_file = os.path.join(self.output_dir, 'UserIdMap')
		self.anonymized_twitter_data_file = os.path.join(self.output_dir, 'AnonymizedTwitterDataSet')


		#FileDescriptor
		self.friends_info_fd = open(self.friends_info_file, 'r')
		self.twitter_data_userid_hash_fd = codecs.open(self.twitter_data_userid_hash_file, 'w', 'utf-8')
		self.anonymized_twitter_data_fd = codecs.open(self.anonymized_twitter_data_file, 'w', 'utf-8')

		#DataStructures
		self.uniq_node_set = set()
		self.uniq_node_list = []
		self.old_id_to_new_id_dict = {}
		self.anonymized_twitter_data = {}


	def run_main(self):
		self.run()

	def run(self):
		friends_info_data = self.friends_info_fd.read()
		self.friends_info_dict = json.loads(friends_info_data)

		#Count unique nodes count
		self.get_uniq_nodes()

		#Assign new ids to the crawled nodes
		self.assign_new_ids()

		#Dump new_id to old_id hash
		self.dump_old_id_to_new_id_dict()
	
		#Generate Anonymized Twitter data
		self.anonymize_twitter_data()

		#Dump anonymized twitter data
		self.dump_anonymize_twitter_data()


	def get_uniq_nodes(self):
		for key, value in self.friends_info_dict.iteritems():
			if key not in self.uniq_node_set:
				self.uniq_node_set.add(key)
			for node in value:
				if node not in self.uniq_node_set:
					self.uniq_node_set.add(node)


	def assign_new_ids(self):
		self.uniq_node_list.extend(list(self.uniq_node_set))
		self.uniq_node_list.sort()

		for new_id, old_id in enumerate(self.uniq_node_list):
			self.old_id_to_new_id_dict[old_id] = new_id
			

	def dump_old_id_to_new_id_dict(self):
		self.twitter_data_userid_hash_fd.write(json.dumps(self.old_id_to_new_id_dict))
		
		self.twitter_data_userid_hash_fd.close()

	def anonymize_twitter_data(self):
		for key, value in self.friends_info_dict.iteritems():
			new_key_id = self.old_id_to_new_id_dict.get(key)
			for node in value:
				new_value_id = self.old_id_to_new_id_dict.get(node)
				self.anonymized_twitter_data.setdefault(new_key_id, []).append(new_value_id)


	def dump_anonymize_twitter_data(self):
		self.anonymized_twitter_data_fd.write(json.dumps(self.anonymized_twitter_data))

		self.anonymized_twitter_data_fd.close()


if __name__ == "__main__":
	ad_obj = AnonymizeData()
	ad_obj.run_main()
