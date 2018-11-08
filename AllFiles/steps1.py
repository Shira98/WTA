#[E->Set of XML retrieved links (relevant) - Top N links (1,2...i...N)] + [Q->The Query] + [NLTG(Set of Internal Links)+HLTG(Set of External Links)].
#Directed graph construction (Internal links):

import xml.etree.ElementTree as ET
import math
from xmlR import *
import numpy as np 

def Docs_names():
	Docs=list()
	file='list.txt'
	#for docs in file:
	with open(file) as f:
		content=f.readlines()
	Docs=[x.strip() for x in content]

	#print(Docs[1])    
	return Docs   


def Root(document_name):
	tree = ET.parse(document_name)
	root = tree.getroot()

	return root


class Di_Graph:
	def __init__(self,L):
		self.docs_root=list()
		self.doc_list=L
		self.original_docs_root=list()
		self.docs_objects=list()
		self.Tree_Set_Creation()

	def Tree_Set_Creation(self):
		#Creating a list of all the tree roots(of each document present in list.txt).
		for i in range(len(self.doc_list)):
			self.docs_root.append(Root(self.doc_list[i]))
			self.original_docs_root.append(Root(self.doc_list[i]))
			self.docs_objects.append(Document())
		
	def Add_Edge(self,Q):
	
		#Pass Q, self.docs_root & self.doc_list onto a function which returns relevant nodes (Marked attributes for retrieved and navigational links).  		
		

		self.add_attrib_files(Q)
		#Add edges b/w navigational links. Combining trees. Storing the inlinks and outlinks through navigational links
		self.nav_elements=[]
		self.retrieved=[]
		temp_list=[]
		self.count_of_retrieved=0

		for root in self.docs_root:
			x=root.findall(".//")

			for i in x:
				#print('hi')

				try:
					#print('hi')
					score=int(i.attrib['retrieved'])
					if score>0:

						doc_index=self.docs_root.index(root)
						temp_list.append(doc_index)
						print(score)
						temp=Retrieved(i,score,doc_index)
						self.retrieved.append(temp)
					#print("nav",i.attrib['nav'])
					if i.attrib['nav']!=None:

						#print(i.get('nav'))
						to_file=self.doc_list.index(i.get('nav'))
						from_file=self.docs_root.index(root)

						temp=Navigational(i,from_file,to_file)
						self.nav_elements.append(temp)
						
						self.retrieved[-1].outlinks.append(to_file)

						self.docs_objects[to_file].inlinks.append(from_file)
						#print('hello')
						self.docs_objects[to_file].inlinks_nodes.append(len(self.retrieved)-1)
						#print(to_file)
						#print(self.doc_list.index(to_file))
						i.append(self.docs_root[to_file])
						self.docs_root[to_file].set('global_root',self.doc_list[from_file])
						#print("hi#")

				except:
					#print("escaped")
					pass

			x=root.findall(".//")
			for i in x:
				print(i.tag)

			self.docs_root[self.docs_root.index(root)]=root
		self.count_of_retrieved=len(list(set(temp_list)))
		#print(len(self.retrieved))
		for node in self.retrieved:
			print(node.element)
		self.Set_links_of_Nodes()


	def Normalization(self): #LS and Content score.
		#Return Relevant score
		pass

	def Distance(self):
		#2-D matrix for all the nodes. Distance b/w each element in it. 
		No_of_nodes=len(self.retrieved)

		self.Distance_matrix=np.zeros((No_of_nodes,No_of_nodes))

		for i in range(No_of_nodes):
			#print(i)
			for j in range(No_of_nodes):
				
				if i!=j:
					Ni=self.retrieved[i]
					Nj=self.retrieved[j]
					distance=self.get_distance_in_doc(Ni,Nj)
					#print(distance)


					
					self.Distance_matrix[i][j]=distance
					#print(self.Distance_matrix[i][j])
					#print(j)
					#print(self.Distance_matrix)
					#self.Distance_matrix[i][j]=self.depth_iter(self.docs_root[Ni.doc])
				else:
					self.Distance_matrix[i][j]=0					

		#print(self.Distance_matrix)

	def get_distance_in_doc(self,Ni,Nj):

		#finding ancestors for Ni,Nj
		#rooti=ET.parse(self.doc_list[Ni.doc]).getroot()
		#rootj=ET.parse(self.doc_list[Nj.doc]).getroot()
		rooti=self.docs_root[Ni.doc]
		global_rooti=self.docs_root[self.doc_list.index(rooti.get('global_root'))]

		ancestors_Ni=self.Get_ancestors(global_rooti,Ni.element)
		rootj=self.docs_root[Nj.doc]
		global_rootj=self.docs_root[self.doc_list.index(rootj.get('global_root'))]
		ancestors_Nj=self.Get_ancestors(global_rootj,Nj.element)

		#finding fist matching ancestor to find distance
		#distance is the sum of heights of elements from matching ancestor
		#print('i',ancestors_Ni,Ni.element.tag)
		#print('j',ancestors_Nj,Nj.element.tag)

		for a in range(len(ancestors_Ni)):
			for b in range(len(ancestors_Nj)):
				if ancestors_Ni[a]==ancestors_Nj[b]:
					#print(a,j,ancestors_Ni[i],ancestors_Nj[j],Ni.element.tag,Nj.element.tag)
					return a+b

		#return list(set(ancestors_Ni).intersection(ancestors_Nj))[0]

	def find_common_ancestor(self,Ni,Nj):

		#finding ancestors for Ni,Nj
		rooti=self.docs_root[Ni.doc]
		global_rooti=self.docs_root[self.doc_list.index(rooti.get('global_root'))]
		ancestors_Ni=self.Get_ancestors(global_rooti,Ni.element)
		#print(ancestors_Ni[-1].element,Ni.doc,global_rooti)
		rootj=self.docs_root[Nj.doc]
		global_rootj=self.docs_root[self.doc_list.index(rootj.get('global_root'))]
		ancestors_Nj=self.Get_ancestors(global_rootj,Nj.element)
		#print(ancestors_Nj[-1].element,Nj.doc,global_rootj)
		#finding fist matching ancestor to find distance
		#distance is the sum of heights of elements from matching ancestor
		for i in range(len(ancestors_Ni)):
			for j in range(len(ancestors_Nj)):
				if ancestors_Ni[i]==ancestors_Nj[j]:
					return ancestors_Ni[i] 

		#return ancestors_Ni[i],ancestors_Ni,ancestors_Nj

	def find_root_from_ancestors(Self,ancestors,node):

		temp=0
		#print(ancestors)
		for  element in ancestors:
			try:
				if element.attrib['root']:
					temp=ancestors.index(element)
					break
			except:
				pass 

		
		return ancestors[temp],ancestors[temp+1]


	def Nodes_in_same_file(self,Ni,Nj):

		if Ni.doc==Nj.doc:
			return True
		return False

	def depth_iter(self,element, tag):
		stack = []
		stack.append(iter([element]))
		while stack:
			print("hi")
			e = next(stack[-1], None)
			if e == None:
				stack.pop()
			else:
				stack.append(iter(e))
				if e.tag == tag:
				   return len(stack)-1

	def Content_Score(self):

		quotient=len(self.doc_list)/(self.count_of_retrieved*1.0)
		self.idf=math.log(quotient)

		for element in self.retrieved:
			element.content_score=self.idf*element.score
			print(element.content_score)


	def Get_ancestors(self,root,node):

		parent_map = {c:p for p in root.iter() for c in p}
		#print(parent_map)
		ancestors=[]
		current=node
		ancestors.append(current)
		#print()
		flag=0
		while True:
			try:
				flag=0
				if parent_map[current]:
					flag=1
					ancestors.append(parent_map[current])
					current=parent_map[current]
			except:
				if flag==0:
					break

		return ancestors

	def Total_Relevance_of_Doc(self):
		#return total
		for element in self.retrieved:
			self.total_rel[element.doc]+=element.relevance_score

	def Set_links_of_Nodes(self):
		#creates links of nodes from docs inlinks
		self.Genrerate_nodes_list()

		for node in self.retrieved:
			node.inlinks+=self.docs_objects[node.doc].inlinks
			node.inlinks_nodes+=self.docs_objects[node.doc].inlinks_nodes+self.docs_objects[node.doc].nodes_list
			node.inlinks_nodes.remove(self.retrieved.index(node))

			for index in node.outlinks:
				node.outlinks_nodes+=self.docs_objects[self.retrieved[index].doc].nodes_list
			node.outlinks_nodes+=self.docs_objects[node.doc].nodes_list
			node.outlinks_nodes.remove(self.retrieved.index(node))

			print(node.inlinks_nodes,node.outlinks_nodes)
			print(node.element)

	def Genrerate_nodes_list(self):
		#Sets the nodes retrieved in a given document in a list
		#print(self.retrieved)
		for node in self.retrieved:
			self.docs_objects[node.doc].nodes_list.append(self.retrieved.index(node))

	def link_score_computation(self): #graph is path weight graph
		# n,n graph where n is no of nodes
		N=len(self.retrieved)
		damp_factor=0.000001
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
				#print(node.content_score)
				link_sum=link_sum+(node.content_score/1+(sum_outL*self.path_weight_nodes(i_node,node)))
			link_sum=link_sum*(damp_factor) +((1-damp_factor)/N)
			self.link_score[no]=link_sum


	def link_weight_H(self,nodei,nodef):

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

	def get_node(self,element):
		for node in self.retrieved:
			if node.element==element:
				return node

	def link_weight_N(self,nodei,docf): #docf is doc object
		doci=nodei.doc
		indexi=self.retrieved.index(nodei)
		sum_x=0.01
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
		print(ancestor.element)
		#if(ancestor==nodei and ancestor==nodef):
			#return 0
		if(ancestor==nodei): 
			#ancestors of nodef
			rootj=self.docs_root[nodef.doc]
			global_rootj=self.docs_root[self.doc_list.index(rootj.get('global_root'))]
			ancestors_Nj=self.Get_ancestors(global_rootj,nodef.element)
			print(nodei.element,nodef.element)
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
			print(path_weight,'rec')
			return path_weight

		if(ancestor.doc==nodei.doc): #anc in nodei's doc
			path_weight=path_weight+self.link_weight_H(nodei,ancestor)+self.path_weight_nvgn(ancestor,nodef,path_weight)
		elif ancestor.doc==nodef.doc:
			path_weight=path_weight+self.link_weight_H(ancestor,nodef)+self.path_weight_nvgn(nodei,ancestor,path_weight)
		else:
			path_weight=path_weight+self.path_weight_nvgn(ancestor,nodef,path_weight)+self.path_weight_nvgn(nodei,ancestor,path_weight)
		print(path_weight,'seq')
		return path_weight

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

	def add_attrib_files(self,Query):

		splitted_Query=Query.split()
		print(splitted_Query)
		for root in self.docs_root:

			index=self.docs_root.index(root)
			self.docs_root[index]=add_root_attribute(root,self.doc_list[index])
			self.docs_root[index]=string_match(splitted_Query,self.doc_list[index],root)
			self.docs_root[index]=nav_links(root,self.doc_list[index],self.doc_list) 

class Document:
	def __init__(self):
		self.inlinks=[]
		self.inlinks_nodes=[]
		self.nodes_list=[]

class Retrieved:
	def __init__(self,e,score,doc):
		self.element=e
		self.score=score 
		self.content_score=None
		self.link_score=None
		self.relevance_score=None
		self.doc=doc
		self.inlinks=[]
		self.inlinks_nodes=[]
		self.outlinks=[]
		self.outlinks_nodes=[]

class Navigational:
	def __init__(self,e,fdoc,tdoc):
		self.element=e
		self.from_doc=fdoc
		self.to_doc=tdoc

class Node:
	def __init__(self):
		self.retrieved=False

#MAIN
Docs_List=Docs_names()
New=Di_Graph(Docs_List)	
Query="Belgian 2008"

New.Add_Edge(Query)
New.Content_Score()
New.Distance()

New.link_score_computation()
print(New.link_score)
#print(New.docs_root[0][2][1])
#print(New.depth_iter(New.docs_root[0],'rank'))

'''
tree=New.docs_root[0]
parent_map = {c.tag:p.tag for p in tree.iter() for c in p}
print(parent_map)
root=New.docs_root[0]
print(root[2][1].tag)
print(New.Get_ancestors(root,root[2][1]))'''
'''
root=ET.parse('draft.xml')
ele=New.docs_root[0][2][1].tag
root=root.getpath(e)
for  ancestor in root.iterancestors():
	print ancestor.tag'''


#Link score computation with IP as the D-graph(Internal links as IP). 
	#Relevant score = intital_weights(Link_i) [Assume till implementation is finished->Vector Based]
	#Path weight = Distance b/w nodes

	#PATH_WEIGHT(Nodei,Nodej):

	#return Link_Score

#Fuzzification(Link_Score, Content_Score->initial_weights)	
#WTF do we do now
