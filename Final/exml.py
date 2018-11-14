'''
def get_inlinks(graph,node):
	a=[] #get no of inner links(other to this node)
	for i in range(len(graph)):
			if(graph[i][node]!=0):
				#means there is link
				a.append(i)
	return a

def get_outlinks(graph,node):
	out=[]
	a=graph[node]
	for i in range(len(a)):
		if(a[i]!=0):#there is a edge
			out.append(i)
	return out
	'''

def link_score_computation(current_RS,damp_factor=0.85): #graph is path weight graph
	# n,n graph where n is no of nodes
	N=len(self.retrieved)
	
	#inlinks=[]
	#outlinks=[]
	link_score=[]
	#calculate inlinks and outlinks
	#for vertex in range(N):
	#	inlinks.append(get_inlinks(path_weight,vertex))
	#	outlinks.append(get_outlinks(path_weight,vertex))

	for no in range(N): #cal link score for each node
		a=[]
		node=self.retrived[no]
		a=node.inlinks_nodes #a conatins list of documents from which node has inlink
		link_sum=0
		for i_node in a: #for each node in inlinks
			out=[]
			sum_outL=0
			out=i_node.inlinks
			for i_onode in out: #for each node in outlinks of i_node in a
				sum_outL=sum_outL+(1/path_weight_nodes(i_onode,i_node))
			link_sum=link_sum+(current_RS[no]/(sum_outL*path_weight_nodes(i_node,node)))
		link_sum=link_sum*(damp_factor) +((1-damp_factor)/N)
		link_score.append(link_sum)

	return link_score

def link_weight_H(nodei,nodef):
	doci=nodei.doc
	docf=nodef.doc
	indexi=self.retrieved.index(nodei)
	indexf=self.retrieved.index(nodef)
	sum_x=0.01


	if(doci==docf): #they are in same doc
		#link weight is hierarchial link weight
		In=len(nodef.inlinks)
		for Ip in nodei.outlinks: #Ip is each document index
			sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
		link_weight=In/sum_x
	return link_weight

def link_weight_N(nodei,docf): #docf is doc object
	doci=nodei.doc
	indexi=self.retrieved.index(nodei)
	sum_x=0
	In=docf.inlinks#no of inlinks to docf
	for Ip in nodei.outlinks: #Ip is doc index
		sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
	link_weight=In/sum_x
	return link_weight

def path_weight_computation(graph,lamda=0.2,dist_graph): #input is NLW and HLW and graph of distance btw 2 nodes
	no_nodes#no of nodes in input = no of retrieved nodes
	no_doc#no of doc
	#path weight computation for all nodes (no_nodes,no_nodes) matrix path_weight=0 means no path
	path_weight=[[0]*no_nodes]*no_nodes

	#inlinks(node) =inlinks(node.doc)
	#outlinks of node=outlinks[node]
def path_weight_nvgn(nodei,nodef,path_weight):
	#find common ancestor of nodei and nodef
	indexi=self.retrieved.index(nodei)
	ancestor=find_common_ancestor(nodei,nodef)
	if(ancestor==nodei): 
		#ancestors of nodef
		ancestors=Get_ancestors(nodef.getroot(),nodef)
		#find first ancestor which is in nodei's doc
		root_nodef,B_root_nodef=find_root_from_ancestors(ansnodef)
		if(B_root_nodef.doc==nodei.doc):
			index_BRN=self.retrieved.index(B_root_nodef)
			path_weight=path_weight+link_weight_N(B_root_nodef,root_nodef)+link_weight_H(nodei,B_root_nodef)*dist_graph[indexi][index_BRN]
		else:
			index_BRN=self.retrieved.index(B_root_nodef)
			path_weight=path_weight+link_weight_N(B_root_nodef,root_nodef)+path_weight_nvgn(nodei,B_root_nodef,path_weight)
		return path_weight

	if(ancestor.doc==nodei.doc): #anc in nodei's doc
		path_weight=path_weight+link_weight_H(nodei,ancestor)+path_weight_nvgn(ancestor,nodef,path_weight)
	elif ancestor.doc==nodef.doc:
		path_weight=path_weight+link_weight_H(ancestor,nodef)+path_weight_nvgn(nodei,ancestor,path_weight)
	else:
		path_weight=path_weight+path_weight_nvgn(ancestor,nodef,path_weight)+path_weight_nvgn(nodei,ancestor,path_weight)
	return path_weight


def path_weight_nodes(nodei,nodef):
	doci=nodei.doc
	docf=nodef.doc
	indexi=self.retrieved.index(nodei)
	indexf=self.retrieved.index(nodef)
	if(doci==docf): #they are in same doc
		path_weight=dist_graph[indexi][indexf] * link_weight_H(nodei,nodef) 
	else:	#diff doc nodei->EP->nodef #there exists a navigational link
		path_weight=path_weight_nvgn(nodei,nodef,path_weight=0)
	return path_weight 
 