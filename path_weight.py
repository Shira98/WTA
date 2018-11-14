def printAllPathsUtil(self, u, d, visited, path,vertices):  
		visited[vertices.index(u)]= True
		path.append(u)
		if u==d: 
			return path
		else:
			for i in u.findall(".//"): 
				if visited[vertices.index(i)]==False: 
					path=self.printAllPathsUtil(i, d, visited, path,vertices)
					if(len(path)!=0):
						return path
		path.pop()
		visited[vertices.index(u)]= False
def printAllPaths(self,u,d,global_root):
	vertices=global_root.findall(".//")
	print(vertices)
	visited =[False]*(len(vertices))
	path = [] 
	path=self.printAllPathsUtil(u, d,visited, path,vertices)
	return path
def path_weight_nvgn(nodei,nodef,path_weight,global_root):
	#traverse down path from i to f
	path=printAllPaths(nodei,nodef,global_root)
	path_weight=0
	N=len(path)
	i=1
	prev=nodei
	while(i<N):
		if(self.prev.doc!=self.path[i].doc):
			#they are in diff doc
			path_weight=path_weight+link_weight_N(prev,path[i])
			prev=path[i]
			i=i+1
		else:
			#they are in same doc
			#if it is retrieved element
			if path[i] in self.retrieved:
				path_weight=path_weight+link_weight_H(prev,path[i])
				prev=path[i]
				i=i+1
			else:
				i=i+1
	return path_weight
def link_score_computation(current_RS,damp_factor=0.85): 
	#link score for computation for all retrived nodes
	N=len(self.retrieved)
	link_score=[]
	for no in range(N): 
		a=[]
		node=self.retrived[no]
		a=node.inlinks_nodes #a conatins list of documents from which node has inlink
		link_sum=0
		for i_node in a: #for each node in inlinks
			out=[]
			sum_outL=0
			out=i_node.inlinks
			for i_onode in out: #for each node in outlinks of i_node in a
				sum_outL=sum_outL+(1/path_weight_nvgn(i_node,i_onode))
			link_sum=link_sum+(current_RS[no]/(sum_outL*path_weight_nvgn(i_node,node)))
		link_sum=link_sum*(damp_factor) +((1-damp_factor)/N)
		link_score.append(link_sum)

	return link_score
def link_weight_H(nodei,nodef):
	#hierarchial link weights
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

def link_weight_N(nodei,nodef): 
	doci=nodei.doc
	docf=nodef.doc
	indexi=self.retrieved.index(nodei)
	sum_x=0
	n_link_weight=0
	In=docf.inlinks #no of inlinks to docf
	for Ip in nodei.outlinks: #Ip is doc index
		sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
	n_link_weight=In/sum_x
	return n_link_weight
