#[E->Set of XML retrieved links (relevant) - Top N links (1,2...i...N)] + [Q->The Query] + [NLTG(Set of Internal Links)+HLTG(Set of External Links)].

#Directed graph construction (Internal links):

import xml.etree.ElementTree as ET
import networkx as nx

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

	#print(root.tag)

	for child in root:
		#print(child.tag, child.attrib)
		pass

	return root


class Di_Graph:
	def __init__(self,L):
		self.docs_root=list()
		self.doc_list=L

		self.Tree_Set_Creation()
	def Tree_Set_Creation(self):

		#Creating a list of all the tree roots(of each document present in list.txt).
		for i in range(len(self.doc_list)):
			self.docs_root.append(Root(self.doc_list[i]))
			
		
	def Add_Edge(self,Q):
	
		#Pass Q, self.docs_root & self.doc_list onto a function which returns relevant nodes (Marked attributes for retrieved and navigational links).  
		self.original_docs_root=self.docs_root
		#self.docs_root=(Q,self.doc_list,self.docs_root)
		
		#Add edges b/w navigational links. Combining trees.
		self.nav_elements=[]
		self.retrieved=[]

		for root in self.docs_root:
			x=root.findall(".//")

			for i in x:

				try:
					if i.attrib['nav']:
					
						to_file=self.doc_list.index(i.get('nav'))
						from_file=self.docs_root.index(root)

						temp=Navigational(i,from_file,to_file)
						self.nav_elements.append(temp)

						i.append(self.docs_root[self.doc_list.index(file_name)])

					if i.attrib['retrieved']:

						doc_index=self.docs_root.index(root)
						score=i.attrib['retrieved']
						temp=Retrieved(i,score,doc_index)

						self.retrieved.append(temp)

				except:
					pass

			self.docs_root[self.doc_list.index(root)]=root


	def Distance(self):
		#2-D matrix for all the nodes. Distance b/w each element in it. 
		No_of_nodes=len(self.retrieved)

		self.Distance_matrix=[[None for i in range(No_of_nodes)] for j in range(No_of_nodes)]

		for i in range(No_of_nodes):
			for j in range(No_of_nodes):

				Ni=self.retrieved[i]
				Nj=self.retrieved[j]


					#distance between hierarchical links
				if Ni.doc==Nj.doc:
					self.Distance_matrix=self.get_distance_in_doc(Ni,Nj)

					#if navigational link exists between nodes, distance between them
				else:

					if self.Doc_has_navigational(Ni):
						pass

	def Doc_has_navigational(self,Ni):

		n=len(self.navigational)
		for 

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

		self.idf=1/sum(r.score for r in self.retrieved)

		for element in self.retrieved:
			element.content_score=self.idf*element.score

	def Get_ancestors(self,root,element):
		parent_map = {c.tag:p.tag for p in root.iter() for c in p}
		ancestors=[]
		current=element.tag
		ancestors.append(current)

		while True:
			try:
				if parent_map[current]:

					ancestors.append(parent_map[current])
					current=parent_map[current]
			except:
				break

		return ancestors

class Retrieved:
	def __init__(self,e,score,doc):
		self.element=e
		self.score=score 
		self.content_score=None
		self.doc=doc

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




