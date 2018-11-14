	def link_weight_N(self,nodei,docf): #docf is doc object
		doci=nodei.doc
		indexi=self.retrieved.index(nodei)
		sum_x=0.1
		In=len(docf.inlinks_nodes)#no of inlinks to docf
		for Ip in nodei.outlinks: #Ip is doc index
			sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
		link_weight=In/sum_x
		return link_weight

	def path_weight_nvgn(self,nodei,nodef,path_weight):
		#find common ancestor of nodei and nodef
		indexi=self.retrieved.index(nodei)
		ancestor_element=self.find_common_ancestor(nodei,nodef)
		ancestor=self.get_node(ancestor_element)
		#print(ancestor.element)
		#if(ancestor==nodei and ancestor==nodef):
			#return 0
		if(ancestor==nodei): 
			#ancestors of nodef
			rootj=self.docs_root[nodef.doc]
			global_rootj=self.docs_root[self.doc_list.index(rootj.get('global_root'))]
			ancestors_Nj=self.Get_ancestors(global_rootj,nodef.element)
			#print(nodei.element,nodef.element)
			#find first ancestor which is in nodei's doc
			root_nodef_element,B_root_nodef_element=self.find_root_from_ancestors(ancestors_Nj,nodef)
			root_nodef=self.get_node(root_nodef_element)
			B_root_nodef=self.get_node(B_root_nodef_element)
			if(B_root_nodef.doc==nodei.doc):
				index_BRN=self.retrieved.index(B_root_nodef)
				path_weight=path_weight+self.link_weight_N(B_root_nodef,nodef)+self.link_weight_H(nodei,B_root_nodef)*self.Distance_matrix[indexi][index_BRN]
			else:
				index_BRN=self.retrieved.index(B_root_nodef)
				path_weight=path_weight+self.link_weight_N(B_root_nodef,root_nodef)+self.path_weight_nvgn(nodei,B_root_nodef,path_weight)
			#print(path_weight,'rec')
			return path_weight

		if(ancestor.doc==nodei.doc): #anc in nodei's doc
			path_weight=path_weight+self.link_weight_H(nodei,ancestor)+self.path_weight_nvgn(ancestor,nodef,path_weight)
		elif ancestor.doc==nodef.doc:
			path_weight=path_weight+self.link_weight_H(ancestor,nodef)+self.path_weight_nvgn(nodei,ancestor,path_weight)
		else:
			path_weight=path_weight+self.path_weight_nvgn(ancestor,nodef,path_weight)+self.path_weight_nvgn(nodei,ancestor,path_weight)
		#print(path_weight,'seq')
		return path_weight


	def link_weight_H(self,nodei,nodef):

		doci=nodei.doc
		docf=nodef.doc
		indexi=self.retrieved.index(nodei)
		indexf=self.retrieved.index(nodef)
		sum_x=0.1

		if(doci==docf): #they are in same doc
			#link weight is hierarchial link weight
			In=len(nodef.inlinks)
			for Ip in nodei.outlinks: #Ip is each document index
				sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
			link_weight=In/sum_x
		return link_weight


	def link_score_computation(self): #graph is path weight graph
		# n,n graph where n is no of nodes
		N=len(self.retrieved)
		damp_factor=0.85
		#inlinks=[]
		#outlinks=[]
		self.link_score=[0 for i in range(N)]
		#calculate inlinkrs and outlinks
		#for vertex in range(N):
		#	inlinks.append(get_inlinks(path_weight,vertex))
		#	outlinks.append(get_outlinks(path_weight,vertex))

		for no in range(N): #cal link score for each node
			a=[]
			node=self.retrieved[no]
			a=node.inlinks_nodes #a conatins list of documents from which node has inlink
			link_sum=0
			for i in a: #for each node in inlinks
				i_node=self.retrieved[i]
				out=[]
				sum_outL=0
				out=i_node.outlinks_nodes
				for i_o in out: #for each node in outlinks of i_node in a
					i_onode=self.retrieved[i_o]
					sum_outL=sum_outL+(1/1+self.path_weight_nodes(i_node,i_onode))
				#print(sum_outL)
				pw=self.path_weight_nodes(i_node,node)
				#print(sum_outL,pw)
				link_sum=link_sum+(node.content_score/1.0*(sum_outL*pw))
			#print(link_sum)
			link_sum=link_sum*(damp_factor) +((1-damp_factor)/N)
			self.link_score[no]=link_sum

	

	def path_weight_nodes(self,i,f):

		nodei=i.element
		nodef=f.element
		doci=i.doc
		docf=f.doc
		indexi=self.retrieved.index(i)
		indexf=self.retrieved.index(f)
		#print(indexi,indexf)
		#print(self.Distance_matrix)
		if(doci==docf): #they are in same doc
			path_weight=self.Distance_matrix[indexi][indexf] * self.link_weight_H(i,f) 
		else:	#diff doc nodei->EP->nodef #there exists a navigational link
			path_weight=self.path_weight_nvgn(i,f,path_weight=0)
		return path_weight 