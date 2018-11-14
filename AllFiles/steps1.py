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

				except:
					#print("escaped")
					pass

			x=root.findall(".//")

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
			#print("hi")
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

			#print(node.inlinks_nodes,node.outlinks_nodes)
			#print(node.element)

	def Genrerate_nodes_list(self):
		#Sets the nodes retrieved in a given document in a list
		#print(self.retrieved)
		for node in self.retrieved:
			self.docs_objects[node.doc].nodes_list.append(self.retrieved.index(node))


	def get_node(self,element):
		for node in self.retrieved:
			if node.element==element:
				return node



	def add_attrib_files(self,Query):

		splitted_Query=Query.split()
		print(splitted_Query)
		for root in self.docs_root:

			index=self.docs_root.index(root)
			self.docs_root[index]=add_filename_attribute(self.doc_list[index],self.docs_root[index])
			self.docs_root[index]=add_root_attribute(root,self.doc_list[index])
			self.docs_root[index]=string_match(splitted_Query,self.doc_list[index],root)
			self.docs_root[index]=nav_links(root,self.doc_list[index],self.doc_list)


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
		return [0]
		path.pop()
		visited[vertices.index(u)]= False


	def link_weight_H(self,nodei,nodef):
		#hierarchial link weights
		print(nodei.attrib['filename'],nodef)
		doci=nodei.get('filename')
		docf=nodef.get('filename')

		#indexi=self.retrieved.index(nodei)
		sum_x=0.01
		n_link_weight=0

		In=self.docs_objects[self.doc_list.index(docf)].inlinks #no of inlinks to docf

		for Ip in self.get_node(nodei).outlinks: #Ip is doc index
			sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
		n_link_weight=len(In)/sum_x
		return n_link_weight

	def link_weight_N(self,nodei,nodef): 

		print(nodei.attrib['filename'],nodef)
		doci=nodei.get('filename')
		docf=nodef.get('filename')

		#indexi=self.retrieved.index(nodei)
		sum_x=0.01
		n_link_weight=0

		In=self.docs_objects[self.doc_list.index(docf)].inlinks #no of inlinks to docf

		for Ip in self.get_node(nodei).outlinks: #Ip is doc index
			sum_x=sum_x+len(self.docs_objects[Ip].inlinks)
		n_link_weight=len(In)/sum_x
		return n_link_weight

	def printAllPaths(self,u,d,global_root):
		vertices=global_root.findall(".//")
		#print(vertices)
		visited =[False]*(len(vertices))
		path = [] 
		path=self.printAllPathsUtil(u, d,visited, path,vertices)
		return path


	def path_weight_nvgn(self,nodei,nodef,global_root):
		#traverse down path from i to f

		path=self.printAllPaths(nodei,nodef,global_root)
		path_weight=0.01
		N=len(path)
		i=1
		prev=nodei
		while(i<N):
			if(prev.get('filename')!=path[i].get('filename')):
				#they are in diff doc
				#print('path:	',path[i])
				path_weight=path_weight+self.link_weight_N(prev,path[i])
				prev=path[i]
				i=i+1
			else:
				#they are in same doc
				#if it is retrieved element
				if path[i] in self.retrieved:
					path_weight=path_weight+((self.link_weight_H(prev,path[i])*self.Distance_matrix[self.get_node(prev)][self.get_node(path[i])]))
					prev=path[i]
					i=i+1
				else:
					i=i+1
		return path_weight

	def find_global_root(self,index1,index2):

		doc1=self.retrieved[index1].doc
		doc2=self.retrieved[index2].doc 

		f1=self.docs_root[doc1].get('global_root')
		f2=self.docs_root[doc1].get('global_root')

		root1=self.docs_root[self.doc_list.index(f1)]
		root2=self.docs_root[self.doc_list.index(f2)]

		if root1 in root2.findall(".//"):
			return root2
		else:
			return root1

	def link_score_computation(self,damp_factor=0.85): 
		#link score for computation for all retrived nodes
		N=len(self.retrieved)
		#link_score=[]

		for no in range(N): 

			a=[]
			node=self.retrieved[no]
			a=node.inlinks_nodes #a conatins list of nodes from which node has inlink
			link_sum=0

			for i in a: #for each node in inlinks

				i_node=self.retrieved[i]
				sum_outL=0.01
				out=i_node.inlinks

				for i_on in out: #for each node in outlinks of i_node in a
					i_onode=self.retrieved[i_on].element
					sum_outL=sum_outL+(1/0.01+self.path_weight_nvgn(i_node.element,i_onode,self.find_global_root(i,i_on)))

				link_sum=link_sum+(self.retrieved[no].content_score/(sum_outL*self.path_weight_nvgn(i_node.element,node.element,self.find_global_root(i,no))))

			link_sum=link_sum*(damp_factor) +((1-damp_factor)/N)
			#link_score.append(link_sum)
			self.retrieved[no].link_score=link_sum
			print(link_sum)


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
Query="Belgian 2008 hello hi"

New.Add_Edge(Query)
New.Content_Score()
New.Distance()

New.link_score_computation()
#print(New.link_score)
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
