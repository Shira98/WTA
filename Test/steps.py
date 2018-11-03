#[E->Set of XML retrieved links (relevant) - Top N links (1,2...i...N)] + [Q->The Query] + [NLTG(Set of Internal Links)+HLTG(Set of External Links)].

#Directed graph construction (Internal links):

import xml.etree.ElementTree as ET

def Parse_Docs():
    Docs=list()
    file='list.txt'
    #for docs in file:
    with open(file) as f:
        content=f.readlines()
    Docs=[x.strip() for x in content]

    print(Docs[1])    
    return Docs   


def Root(document_name):
    document_name='draft.xml'
    tree = ET.parse(document_name)
    root = tree.getroot()

    print(root.tag)

    for child in root:
        print(child.tag, child.attrib)

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
            
        
    #def Query_result():
    
        #Mark nodes that have been returned by the query Q.        


class Node:
    def __init__(self):
        self.retrieved=False

#MAIN
Docs_List=Parse_Docs()
New=Di_Graph(Docs_List)	

#Link score computation with IP as the D-graph(Internal links as IP). 
	#Relevant score = intital_weights(Link_i) [Assume till implementation is finished]
	#Path weight = Distance b/w nodes

	#PATH_WEIGHT(Nodei,Nodej):

	#return Link_Score

#Fuzzification(Link_Score, Content_Score->initial_weights)	
	#WTF do we do now




