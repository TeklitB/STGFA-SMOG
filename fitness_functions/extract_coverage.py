import os
from lxml import html
from bs4 import UnicodeDammit
import settings

def extract_code_coverage(packagename):
    report_path = settings.ACVTOOL_WDIR+"report/"+packagename+"/report/index.html"
    if not os.path.exists(report_path):
        return (0,0,0)
    with open(report_path, 'rb') as file:
        content = file.read()
        doc = UnicodeDammit(content, is_html=True)

	parser = html.HTMLParser(encoding=doc.original_encoding)
	root = html.document_fromstring(content, parser=parser)
	# Extract line, method, and class coverage
    missed_lines = int(root.xpath('/html/body/table/tfoot/tr/td[4]/text()')[0].strip())
    total_lines = int(root.xpath('/html/body/table/tfoot/tr/td[5]/text()')[0].strip())
    missed_methods = int(root.xpath('/html/body/table/tfoot/tr/td[6]/text()')[0].strip())
    total_methods = int(root.xpath('/html/body/table/tfoot/tr/td[7]/text()')[0].strip())
    missed_classes = int(root.xpath('/html/body/table/tfoot/tr/td[8]/text()')[0].strip())
    total_classes = int(root.xpath('/html/body/table/tfoot/tr/td[9]/text()')[0].strip())

    # Calculate lines covered, methods covered, and classes covered
    covered_lines = (float((total_lines - missed_lines))/total_lines)*100
    covered_methods = (float((total_methods - missed_methods))/total_methods)*100
    covered_classes = (float((total_classes - missed_classes))/total_classes)*100
    print("Line coverage: {0} Method coverage: {1} Class Coverage: {2}".format(covered_lines, covered_methods, covered_classes))
    return (covered_lines, covered_methods, covered_classes)


if __name__ =="__main__":
    pathto = settings.ACVTOOL_WDIR+"report/org.scoutant.blokish/report/index.html"
    print(extract_code_coverage(pathto))