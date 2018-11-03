#input ia all roots of xml files and string (list of words)
#output will be a 2d list saying which tags are retured
#check the condition for returning subtree
#compute initial scores will be done with updated attributes
#searching in single file

#add retrieved attribute to all tags
def add_attribute(root):
	root.set('retrieved', '0')
	if(len(root)!=0):
		for child in root:
			add_attribute(child)
	tree.write('q1.xml')

def update_attribute(root):
	att_value=int(root.get('retrieved'))
	att_value=att_value+1
	root.set('retrieved',str(att_value))
	tree.write('q1.xml')
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

import xml.etree.ElementTree as ET
tree=ET.parse('q1.xml')
root=tree.getroot()
l=['4','2011','59900']
add_attribute(root)
string_match(l,root)

		




