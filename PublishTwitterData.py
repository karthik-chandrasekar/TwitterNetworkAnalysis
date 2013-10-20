import  logging
import networkx as nx

class SocialNetworkAnalysis:
	def __init__(self):
	
		#Filenames
		self.twitter_data_edge_list = 'twitter_data_edge_list'	
		self.logger_file = 'crawl_twitter.log'

	def run(self):

		self.initialize_logger()
		self.get_graph_from_edge_list()
		self.network_measures()

	def initialize_logger(self):

		logging.basicConfig(filename=self.logger_file, level=logging.INFO)
		logging.info("Initialized logger")	


	def get_graph_from_edge_list(self):

		logging.info("Forming graph from edge list")
		self.G = nx.read_edgelist(self.twitter_data_edge_list, create_using=nx.DiGraph())

	def network_measures(self):

		self.get_connected_comp()
		self.dump_largest_sub_graph()
		self.p1()
		self.p2()
		self.p3()

	def get_connected_comp(self):

		#Compute the largest connected component
		logging.info("Get connected comp")
		self.SG = nx.connected_component_subgraphs(self.G.to_undirected())[0]

	def dump_largest_sub_graph(self):

		logging.info("Logging largest sub graph")
		nx.write_edgelist(self.SG, 'largest_sub_graph_edge_list')


	def p1(self):

		logging.info( "Inside p1")
		self.graph_diameter()
		self.count_3_cycles()

	def p2(self):

		logging.info("Inside p2")
		self.local_clustering_coefficient()
		self.global_clustering_coefficient()
		self.in_degree_centrality()
		self.eigen_vector_centrality()
		self.pagerank()

	def p3(self):
		logging.info("Inside p3")
		self.find_minimum_spanning_tree()

	def graph_diameter(self):

		logging.info("Inside calculating graph dia")
		diameter = nx.diameter(self.SG)
		logging.info("Diameter of the graph is %s" % (diameter))
	
	def count_3_cycles(self):

		#Compute no of 3 cycles
		logging.info("Count the number of cycles of length 3 present")
		three_cycle_list = []
		all_cycle_list = list(nx.simple_cycles(self.G))
		for cycle in all_cycle_list:
			if len(cycle) == 3:
				three_cycle_list.append(cycle)

		logging.info("Length of three cycle is %s" % (len(three_cycle_list)))
		three_cycle_list = []

	

	def local_clustering_coefficient(self):

		#Compute the local clustering coefficient
		logging.info("Compute the local clustering coefficient")
		clustering_values_dict = nx.clustering(self.SG)
		logging.info("Clustering value dict is %s" % (len(clustering_values_dict.keys())))

		logging.info("Finding average of local clustering coeff")

		local_clust_coeff_values = clustering_values_dict.values()
		logging.info("Avg local clustering coeff is %s" % (sum(local_clust_coeff_values)/len(local_clust_coeff_values)))


	def global_clustering_coefficient(self):

		#Compute the global clustering coefficient
		logging.info("Gloabl clustering coeffcient")
		avg_clustering_value = nx.average_clustering(self.SG)
		logging.info("Avg clustering value is %s" % (avg_clustering_value))

	def in_degree_centrality(self):

		#Compute the in degree centrality of the graph
		logging.info("Inside degree centrality")
		indegree_dict = nx.in_degree_centrality(self.G)
		logging.info("In degree dic length %s" % (len(indegree_dict.keys())))
	
		indegree_sorted_list = sorted(indegree_dict.items(), key=lambda x:x[1], reverse=True)[:3]
		
		for a,b in indegree_sorted_list:
			logging.info("In degree cent of %s is %s" % (a,b))
	
		indegree_dict = {}



	def eigen_vector_centrality(self):

		#Compute the eigen vector centrality of the graph
		logging.info("Inside eigne vector centrality module")
		eigenvector_centrality_dict = nx.eigenvector_centrality_numpy(self.G)		
		logging.info("Eigen vector centrality dict count is %s " % (len(eigenvector_centrality_dict.keys())))
		
		eigen_vector_sorted_list = sorted(eigenvector_centrality_dict.items(), key=lambda x:x[1], reverse=True)[:3]
	
		for a,b in eigen_vector_sorted_list:
			logging.info("Eigen vector cent for %s is %s" % (a,b))
		
		eigenvector_centrality_dict = {}

	def pagerank(self):

		#Compute the page rank of the graph
		logging.info("Inside pagerank module")
		pagerank_dict = nx.pagerank_numpy(self.G)	
		logging.info("Page rank dict length is %s" % (len(pagerank_dict.values())))
		
		pagerank_sorted_list = sorted(pagerank_dict.items(), key=lambda x:x[1], reverse=True)[:3]
		
		for a,b in pagerank_sorted_list:
			logging.info("Page rank cent for %s is %s" % (a, b))

		pagerank_dict = {}


	def find_minimum_spanning_tree(self):

		#Compute the minimum spanning tree
		logging.info("Minimum spanning tree ")
		mst = nx.minimum_spanning_tree(self.SG)

		logging.info("The weight of mst")
		logging.info(len(mst.edges(data=True)))
		

if __name__ == "__main__":
	san  = SocialNetworkAnalysis()
	san.run()
