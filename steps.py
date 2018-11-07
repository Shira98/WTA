#[E->Set of XML retrieved links (relevant) - Top N links (1,2...i...N)] + [Q->The Query] + [NLTG(Set of Internal Links)+HLTG(Set of External Links)].

#Directed graph construction (Internal links):

import xml.etree.ElementTree as ET
import networkx as nx
import math

def Parse_Docs():
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
		
		#self.docs_root=(Q,self.doc_list,self.docs_root)
		#self.nodes_graph=[]
		#Add edges b/w navigational links. Combining trees.
		self.nav_elements=[]
		self.retrieved=[]
		temp_list=[]
		self.count_of_retrieved=0

		for root in self.docs_root:
			x=root.findall(".//")

			for i in x:

				try:
					if i.attrib['retrieved']:

						doc_index=self.docs_root.index(root)
						temp_list.append(doc_index)
						score=i.attrib['retrieved']
						temp=Retrieved(i,score,doc_index)
						self.retrieved.append(temp)

					if i.attrib['nav']:
					
						to_file=self.doc_list.index(i.get('nav'))
						from_file=self.docs_root.index(root)

						temp=Navigational(i,from_file,to_file)
						self.nav_elements.append(temp)
						
						self.retrieved[-1].outlinks.append(to_file)
						self.docs_objects[to_file].inlinks.append(from_file)

						i.append(self.docs_root[self.doc_list.index(file_name)])

					

				except:
					pass


		self.count_of_retrieved=len(list(set(temp_list)))

	'''def Check_existenece(self,element):

		for root in self.nodes_graph:
			if root.iselement(element):
				return self.nodes_graph.index(root)'''


	def Normalization(self): #LS and Content score.
		#Return Relevant score
		pass

	def Distance(self):
		#2-D matrix for all the nodes. Distance b/w each element in it. 
		No_of_nodes=len(self.retrieved)

		self.Distance_matrix=[[None for i in range(No_of_nodes)] for j in range(No_of_nodes)]
		self.Pth
		for i in range(No_of_nodes):
			for j in range(No_of_nodes):

				Ni=self.retrieved[i]
				Nj=self.retrieved[j]

				self.Distance_matrix[i][j]=self.get_distance_in_doc(Ni,Nj)

	def get_distance_in_doc(self,Ni,Nj):

		#finding ancestors for Ni,Nj
		ancestors_Ni=self.Get_ancestors(Ni.getroot(),Ni)
		ancestors_Nj=self.Get_ancestors(Nj.getroot(),Nj)

		#finding fist matching ancestor to find distance
		#distance is the sum of heights of elements from matching ancestor
		for i in range(len(ancestors_Ni)):
			for j in range(len(ancestors_Nj)):
				if ancestors_Ni[i]==ancestors_Nj[j]:
					return i+j

		#return list(set(ancestors_Ni).intersection(ancestors_Nj))[0]

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

		quotient=len(doc_list)/self.count_of_retrieved
		self.idf=math.log(quotient)

		for element in self.retrieved:
			element.content_score=self.idf*element.score

	def Get_ancestors(self,root,element):
		parent_map = {c:p for p in root.iter() for c in p}
		ancestors=[]
		current=element
		ancestors.append(current)

		while True:
			try:
				if parent_map[current]:

					ancestors.append(parent_map[current])
					current=parent_map[current]
			except:
				break

		return ancestors

	def Total_Relevance_of_Doc(self):
		#return total
		for element in self.retrieved:
			self.total_rel[element.doc]+=element.relevance_score

	def Set_links_of_Nodes(self):

		for node in self.retrieved:
			node.inlinks+=self.docs_objects[node.doc].inlinks

class Document:
	def __init__(self):
		self.inlinks=[]

class Retrieved:
	def __init__(self,e,score,doc):
		self.element=e
		self.score=score 
		self.content_score=None
		self.link_score=None
		self.relevance_score=None
		self.doc=doc
		self.inlinks_list=[]
		self.outlink_list=[]
		self.inlinks=0
		self.outlinks=0

class Navigational:
	def __init__(self,e,fdoc,tdoc):
		self.element=e
		self.from_doc=fdoc
		self.to_doc=tdoc

class Node:
	def __init__(self):
		self.retrieved=False

#MAIN
Docs_List=Parse_Docs()
New=Di_Graph(Docs_List)	
Query='2008'
#New.Add_Edge(Query)
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
