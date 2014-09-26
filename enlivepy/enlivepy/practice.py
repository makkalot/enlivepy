from lxml import etree

root = etree.Element("root")
print root.tag

root.append(etree.Element("child1"))

child2 = etree.SubElement(root, "child2")
child3 = etree.SubElement(root, "child3")

#print etree.tostring(root, pretty_print=True)

#elements are like lists
child = root[0]
print child.tag
print child.getparent().tag

#check if has children
print len(root)

#The have attributes which is nice
root.set("hello", "Huhu")
#print etree.tostring(root, pretty_print=True)
print root.get("hello")

root.text = "Some Content"
print etree.tostring(root, pretty_print=True)
