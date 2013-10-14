import json
import networkx as nx

class CrawledInput:
	def __init__(self):
	
		#Filenames
		self.friends_info_file = 'crawled_nodes_output'
		
		#FileDescriptor
		self.friends_info_fd = open(self.friends_info_file, 'r')

		#DataStructures
		self.friends_info_dict = {}
		self.uniq_node_set = set()
		self.adjacency_list = []

	def run(self):
		friends_info_data = self.friends_info_fd.read()
		self.friends_info_dict = json.loads(friends_info_data)

		#Count unique nodes count
		self.get_uniq_node_count()

		#Display unique nodes count
		print "Unique number of user node is %s "  % (len(self.uniq_node_set))

		#Generate adj list from json output
		self.generate_adj_list()

		#Parse adjlist and form graph
		self.get_graph()

		self.network_measures()


	def get_graph(self):
		self.G = nx.parse_adjlist(self.adjacency_list, nodetype=int)
		print (len(self.G.nodes()))
		print (len(self.G.edges()))


	def generate_adj_list(self):
		for key, value in self.friends_info_dict.iteritems():
			tmp = ''
			tmp = '%s' % (key)
			for node in value:
				tmp = '%s %s' % (tmp, node)
			self.adjacency_list.append(tmp)

		
	def get_uniq_node_count(self):
		for key, value in self.friends_info_dict.iteritems():
			if key not in self.uniq_node_set:
				self.uniq_node_set.add(key)
			for node in value:
				if node not in self.uniq_node_set:
					self.uniq_node_set.add(node)



	def network_measures(self):
		self.betweeness_centrality()
		self.closeness_centrality()

	def betweeness_centrality(self):
		betweenness = nx.algorithms.centrality.betweenness_centrality(self.G)
		print 'Betweenness computations complete.'

	def closeness_centrality(self):
		closeness = nx.algorithms.centrality.closeness_centrality(self.G)
		print 'Closeness computations complete.'



if __name__ == "__main__":
	ci  = CrawledInput()
	ci.run()
