'''This file implements the Branch and Bound method to find minimum vertex cover for a given input graph.

Author: Sangy Hanuamsagar, Team 25

'''

import networkx as nx
import operator
import time

# USE THE ADJACENCY LIST TO CREATE A GRAPH
def create_graph(adj_list):
	G = nx.Graph()
	for i in range(len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i + 1, j)
	return G

# BRANCH AND BOUND FUNCTION to find minimum VC of a graph
"""The algorithm is summarized as follows:

Every vertex is considered as having one of two states: 1 or 0
State 1---> Vertex is a part of Vertex Cover (VC) 
State 0---> Vertex is not a part of Vertex Cover (VC) whihc means all its neighbors HAVE to be in VC

Frontier Set: contains the set of candiadate vertices for a subproblem. Each entry is a tuple list comprising of (vertex ID, state, parent in searching tree) 

CurG: subproblem of current graph after removing explored nodes 
CurVC: Current VC found in particular instance of search
OptVC: Best (i.e. minimum) value of |CurVC| at any given point form start

Bounds to Solutions:
Upper Bound: Initially set to number of nodes and updated to size of current solution (i.e. size of minimum vertex cover found in search)

Lower bound: |Current VC| + LB(CurG)
LB(CurG)=sum of edges in CurG / maximum node degree in CurG

Stages of Implementation:
1) Choose candidate node (vi)
	Each search is started from the node with highest degree in CurG, as it represents the most promising node to be included in the VC. This node is stored in the last index of Frontier set, and accessed using Frontier.pop().

	Appened (vi,1) and (vi,0) to CurVC as a tuple= (vertex,state)


2)  If State==1: Remove from CurG 
	This removes the node and its edges from CurG
	
	If state==0, Add all neighbors of vi to CurVC and remove vi from CurG

3) Consider CurG
	If No more edges in CurG-->Candidate solution is found (CurVC accounts for all edges). 
		Check to see if |CurVC| lesser than |OptVC| (and update OptVC if true, otherwise backtrack to find new path) 
	Else Update Lower bound and prune as necessary.
		If Lowerbound<Upperbound, solution is possible
			Append next highest degree node in CurG to Frontier set 
		Else, there is no better solution in this search sapce, so can be pruned from CurG. Backtrack to find new path.

4) Backtracking
	After reaching the end of a path, we need to backtrack to consider a new path. To do this, we have to undo the changes made to CurG and CurVC, which is where the parent item of each tuple in Frontier is handy.
	
	If the parent node is in the VC, then 
		we remove the last few elements from CurVC that were added after teh parent node was discovered and add the corresponing nodes+edges back to CurG. This basically 'undoes the mistakes' to CurG...
	Else then the parent must be (-1,-1) i.e. start of the graph or root node
		Reset CurG to G and CurVC to empty 

When Frontier Set==empty, the whole graph and all possible solutions have been examined.G

End
"""

def BnB(G):
	#RECORD START TIME
	start_time=time.time()
	end_time=start_time
	delta_time=end_time-start_time
	# times=[]    #list of times when solution is found, tuple=(VC size,delta_time)

	# INITIALIZE SOLUTION VC SETS AND FRONTIER SET TO EMPTY SET
	opt_vc = []
	cur_vc = []
	frontier = []
	neighbor = []

	# ESTABLISH INITIAL UPPER BOUND
	upperbound = G.number_of_nodes()
	# print('Initial UpperBound:', upperbound)

	cur_g = G.copy()  # make a copy of G
	# sort dictionary of degree of nodes to find node with highest degree
	v = find_maxdeg(cur_g)

	# APPEND (V,1,(parent,state)) and (V,0,(parent,state)) TO FRONTIER
	frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
	frontier.append((v[0], 1, (-1, -1)))

	while frontier!=[]:
		(vi,state,parent)=frontier.pop() #set current node to last element in Frontier
		
		backtrack = False

		if state == 0:  # if vi is not selected, state of all neighbors=1
			neighbor = cur_g.neighbors(vi)  # store all neighbors of vi
			for node in list(neighbor):
				cur_vc.append((node, 1))
				cur_g.remove_node(node)  # node is in VC, remove neighbors from CurG
		elif state == 1:  # if vi is selected, state of all neighbors=0
			cur_g.remove_node(vi)  # vi is in VC,remove node from G
		else:
			pass

		cur_vc.append((vi, state))
		cur_vc_size = vc_size(cur_vc)

		if cur_g.number_of_edges() == 0:  # end of exploring, solution found
			if cur_vc_size < upperbound:
				opt_vc = cur_vc.copy()
				# print('Current Opt VC size', cur_vc_size)
				upperbound = cur_vc_size
				# times.append((cur_vc_size,time.time()-start_time))
			backtrack = True
				
		else:   #partial solution
			cur_lb = lowerbound(cur_g) + cur_vc_size

			if cur_lb < upperbound:  # worth exploring
				vj = find_maxdeg(cur_g)
				frontier.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
				frontier.append((vj[0], 1, (vi, state)))
			else:
				# end of path, will result in worse solution,backtrack to parent
				backtrack=True


		if backtrack==True:
			if frontier != []:	#otherwise no more candidates to process
				nextnode_parent = frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))

				# backtrack to the level of nextnode_parent
				if nextnode_parent in cur_vc:
					
					id = cur_vc.index(nextnode_parent) + 1
					while id < len(cur_vc):	#undo changes from end of CurVC back up to parent node
						mynode, _ = cur_vc.pop()	#undo the addition to CurVC
						cur_g.add_node(mynode)	#undo the deletion from CurG
						
						# find all the edges connected to vi in Graph G
						# or the edges that connected to the nodes that not in current VC set.
						
						cur_vc_nodes = list(map(lambda t:t[0], cur_vc))
						for nd in G.neighbors(mynode):
							if (nd in cur_g.nodes()) and (nd not in cur_vc_nodes):
								cur_g.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

				elif nextnode_parent == (-1, -1):
					# backtrack to the root node
					cur_vc.clear()
					cur_g = G.copy()
				else:
					print('error in backtracking step')

		end_time=time.time()
		delta_time=end_time-start_time
		# if delta_time>T:
		# 	print('Cutoff time reached')

	return opt_vc, delta_time

#TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
def find_maxdeg(g):
	deglist = dict(g.degree())
	deglist_sorted = sorted(deglist.items(), reverse=True, key=operator.itemgetter(1))  # sort in descending order of node degree
	v = deglist_sorted[0]  # tuple - (node,degree)
	return v

#EXTIMATE LOWERBOUND
def lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=ceil(lb)
	return lb


def ceil(d):
    """
        return the minimum integer that is bigger than d
    """ 
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    

#CALCULATE SIZE OF VERTEX COVER (NUMBER OF NODES WITH STATE=1)
def vc_size(VC):
	# VC is a tuple list, where each tuple = (node_ID, state, (node_ID, state)) vc_size is the number of nodes which has state == 1

	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size