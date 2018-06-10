import lxml.etree as ET

# xsl_filename = "questionWithoutNotice.xsl"
# xsl_filename = "xslOld.xsl"
xsl_filename = "grabBill.xsl"

xml_filename = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/2012/2012-06-19.xml"
#xml_filename = "example.xml"
# xml_filename = "/Users/jeremypattison/LargeDocument/ResearchProjectData/house_hansard/1999/1999-06-22.xml"




dom = ET.parse(xml_filename)

print dom

xslt = ET.parse(xsl_filename)

print xslt

transform = ET.XSLT(xslt)

newdom = transform(dom)

print(ET.tostring(newdom, pretty_print=True))