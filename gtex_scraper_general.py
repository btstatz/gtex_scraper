import sys
from lxml import html
from bs4 import BeautifulSoup

outer_divs = None
sample_dict = {}
for index, file in enumerate(sys.argv):
	if index > 0:
		a = open(file, 'r').read()
		soup = BeautifulSoup(a, 'lxml')
		if index == 1:
			outer_divs = soup.find_all("div", style="display: flex; white-space: nowrap; font-weight: 400; background-color: rgb(249, 249, 249);")
			outer_divs += soup.find_all("div", style="display: flex; white-space: nowrap; font-weight: 400; background-color: rgb(255, 255, 255);")
		else:
			outer_divs += soup.find_all("div", style="display: flex; white-space: nowrap; font-weight: 400; background-color: rgb(249, 249, 249);")
			outer_divs += soup.find_all("div", style="display: flex; white-space: nowrap; font-weight: 400; background-color: rgb(255, 255, 255);")

for row in outer_divs:
	row_text = []
	for x in row:
		row_text.append(x.get_text())
	sample_id = row_text[4]
	sample_dict[sample_id] = [0, 0]
	sample_description = row_text[6]

	if sample_description.find("muscularis") >= 0:
		sample_dict[sample_id][0] = 1
	if sample_description.find("mucosa") >= 0 and sample_description.find("no mucosa") == -1 and sample_description.find("trimmed") == -1:
		sample_dict[sample_id][1] = 2
	if sample_description.find("trace") >= 0 or sample_description.find("minute") >= 0:
		sample_dict[sample_id][1] = 1

with open('gtex_categorized.csv', 'w') as f:
	for sample_id in sample_dict:
		f.write(sample_id + "\t" + str(sample_dict[sample_id][0]) + "\t" + str(sample_dict[sample_id][1]) + "\n")