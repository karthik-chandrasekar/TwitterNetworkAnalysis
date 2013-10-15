import json
import networkx as nx

class CrawledInput:
	def __init__(self):
	
		#Filenames
		self.friends_info_file = 'crawled_nodes_output'   #Don't hard code the file names. 
		
		#FileDescriptor
		self.friends_info_fd = open(self.friends_info_file, 'r')

		#DataStructures
		self.friends_info_dict = {}
		self.uniq_node_set = set()
		self.adjacency_list = []

		#GlobalVariables
		self.NODE_LIMIT = 5

	def run(self):
		friends_info_data = self.friends_info_fd.read()
		self.friends_info_dict = json.loads(friends_info_data)

		#Count unique nodes count
		self.get_uniq_nodes()

		#Display unique nodes count
		print "Unique number of user node is %s "  % (len(self.uniq_node_set))

		#Generate adj list from json output
		self.generate_adj_list_without_limit()

		#Parse adjlist and form graph
		self.get_graph()

		self.network_measures()


	def get_graph(self):

		self.G = nx.DiGraph(nx.parse_adjlist(self.adjacency_list, nodetype=int))


	def generate_adj_list(self):
		i=0
		for key, value in self.friends_info_dict.iteritems():
			tmp = ''
			tmp = '%s' % (key)
			for node in value:
				tmp = '%s %s' % (tmp, node)
			i +=1
			if i<self.NODE_LIMIT:
				self.adjacency_list.append(tmp)
			else:
				break

	def generate_adj_list_without_limit(self):
		for key, value in self.friends_info_dict.iteritems():
			tmp = ''
			tmp = '%s' % (key)
			for node in value:
				tmp = '%s %s' % (tmp, node)
				self.adjacency_list.append(tmp)


		
	def get_uniq_nodes(self):
		for key, value in self.friends_info_dict.iteritems():
			if key not in self.uniq_node_set:
				self.uniq_node_set.add(key)
			for node in value:
				if node not in self.uniq_node_set:
					self.uniq_node_set.add(node)

	def network_measures(self):
		self.p1()
		self.p2()

	def p1(self):
		self.graph_diameter()
		self.count_3_cycles()

	def p2(self):
		#self.local_clustering_coefficient()
		#self.global_clustering_coefficient()
		self.degree_centrality()
		self.eigen_vector_centrality()
		self.pagerank()


	def graph_diameter(self):
		diameter = nx.diameter(self.G)
		print "Diameter of the graph is %s" % (diameter)
	
	def count_3_cycles(self):
		three_cycle_list = []
		all_cycle_list = list(nx.simple_cycles(self.G))
		for cycle in all_cycle_list:
			if len(cycle) == 3:
				three_cycle_list.append(cycle)

		print "Length of three cycle is %s" % (len(three_cycle_list))

	def local_clustering_coefficient(self):
		clustering_values_dict = nx.clustering(self.G)
		print "Clustering value dict is %s" % (len(clustering_values_dict.keys()))


	def global_clustering_coefficient(self):
		avg_clustering_value = nx.average_clustering(self.G)
		print "Avg clustering value is %s" % (avg_clustering_value)

	def degree_centrality(self):
		indegree_dict = nx.in_degree_centrality(self.G)
		print "In degree dic length %s" % (len(indegree_dict.keys()))

	def count_triangles(self):
		graph_triangles = nx.triangles(self.G)
		print "3 cycle graph count %s" % (len(graph_triangles.keys()))

	def eigen_vector_centrality(self):
		eigenvector_centrality_dict = nx.eigenvector_centrality_numpy(self.G)		
		print "Eigen vector centrality dict count is %s " % (len(eigenvector_centrality_dict.keys()))

	def pagerank(self):
		pagerank_dict = nx.pagerank_numpy(self.G)	
		print "Page rank dict length is %s" % (len(pagerank_dict.values()))

if __name__ == "__main__":
	ci  = CrawledInput()
	ci.run()
