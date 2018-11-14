#input ia all roots of xml files and string (list of words)
#output will be a 2d list saying which tags are retured
#check the condition for returning subtree
#compute initial scores will be done with updated attributes
#searching in single file

#add retrieved attribute to all tags
def add_root_attribute(root,file_name):
	root.set('root', file_name)
	root.set('global_root', file_name)
	tree=ET.parse(file_name)
	tree.write(file_name)
	return root

def add_attribute(root,file_name):
	tree=ET.parse(file_name)
	root.set('retrieved', '0')
	if(len(root)!=0):
		for child in root:
			add_attribute(child,file_name)
	tree.write(file_name)

def update_attribute(root,file_name):
	att_value=int(root.get('retrieved'))
	att_value=att_value+1
	root.set('retrieved',str(att_value))
	tree=ET.parse(file_name)
	tree.write(file_name)

def update_parent_AttV(root,file_name):
	flag=1
	if(len(root)!=0):
		for child in root:
			if(child.text!=None):
				if(int(child.get('retrieved')) == 0):
					flag=0
			update_parent_AttV(child,file_name)
		if(flag==1):
			#all children retrieved value!=0
			update_attribute(root,file_name)

def string_match(list,file_name,root):
	#match all words in list
	#check till end of the file
	add_attribute(root,file_name) #make all retrieves 
	for word in list:
		#find if word is in that document of root
		#print(word)
		word_find(word,root,file_name)
	update_parent_AttV(root,file_name)

	return root

def add_filename_attribute(file_name,root):
	elements=root.findall(".//")
	for element in elements:
		#add attribute called filename to each attribute
		element.set('filename', file_name)
		#tree.write(file_name)
	root.set('filename', file_name)


def word_find(word,root,file_name):
	#if word in root.text
		text=root.text
		if(text!=None):
			#print(text)
			if(text.find(word)!=-1):
				update_attribute(root,file_name)
		for child in root:
				 word_find(word,child,file_name)
def nav_links(root,file_name,doc_list):
	k=[]
	tree=ET.parse(file_name)
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
			nav_links(child,file_name,doc_list)
	#return a
	return root


import xml.etree.ElementTree as ET
'''tree=ET.parse(file_name)

root=tree.getroot()
l=['4','2011','59900']
a=[]
a=nav_links(root,a)
print(a)
#string_match(l,root)'''
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

		




