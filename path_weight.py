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
