#input ia all roots of xml files and string (list of words)
#output will be a 2d list saying which tags are retured
#check the condition for returning subtree
#compute initial scores will be done with updated attributes
#searching in single file

#add retrieved attribute to all tags
def add_root_attribute(file_name):
	root.set('root', file_name)
	tree.write(file_name)

def add_attribute(root):
	root.set('retrieved', '0')
	if(len(root)!=0):
		for child in root:
			add_attribute(child)
	tree.write(file_name)

def update_attribute(root):
	att_value=int(root.get('retrieved'))
	att_value=att_value+1
	root.set('retrieved',str(att_value))
	tree.write(file_name)

def update_parent_AttV(root):
	flag=1
	if(len(root)!=0):
		for child in root:
			if(child.text!=None):
				if(int(child.get('retrieved')) == 0):
					flag=0
			update_parent_AttV(child)
		if(flag==1):
			#all children retrieved value!=0
			update_attribute(root)

def string_match(list,root):
	#match all words in list
	#check till end of the file
	add_attribute(root) #make all retrieves 
	for word in list:
		#find if word is in that document of root
		#print(word)
		word_find(word,root)
	update_parent_AttV(root)

def word_find(word,root):
	#if word in root.text
		text=root.text
		if(text!=None):
			#print(text)
			if(text.find(word)!=-1):
				update_attribute(root)
		for child in root:
				 word_find(word,child)
def nav_links(root,file_name,doc_list):
	k=[]
	#check in root
	#print(root)
	nav_value=root.get('{http://www.w3.org/1999/xlink}href')
	#print(nav_value)
	if(nav_value!=None): #Means it has some link'
		if(nav_value in doc_list):
			root.set('nav',nav_value)
			tree.write(file_name)
		#a.append([root,nav_value])
	for child in root:
			nav_links(child,a)
	#return a


import xml.etree.ElementTree as ET
tree=ET.parse(file_name)

root=tree.getroot()
l=['4','2011','59900']
a=[]
a=nav_links(root,a)
print(a)
#string_match(l,root)
'''
import xml.etree.ElementTree as ET
tree=ET.parse(file_name)
root=tree.getroot()
#print(root.text)
tag=root.tag
#print(tag)

att_value=root[0].get('{http://www.w3.org/1999/xlink}href')
print(att_value)

#print(root.attrib)
'''

		




