import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

def getHTML(url):
    try:
    	head = {}
    	head['user_agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0)'
    	req = urllib2.Request(url, headers=head)
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.URLError as e:
        print e.reason 

def getWikitables(html):
	soup = BeautifulSoup(html)
	tables = soup.find_all(class_='wikitable')
	wikitables = []
	for table in tables:
		if 'wikitable' in table['class']:
			wikitables.append(table)
	return wikitables

def write(html):
	outputfile = codecs.open("file.txt",mode="wb",encoding='utf8')
	outputfile.write("%s" % html)

def createSQL(list):
	query = ""
	for item in list:
	    query = query +  "INSERT INTO `cities` (`city`,`state`) VALUES ('%s','%s');" %((item['city']).replace("'", "\\'"),item['state'])
	print query
	return query

def writeSQL(sql):
	outputfile = codecs.open("query.sql","wb",encoding="utf-8")
	outputfile.write("%s" % sql)

def main():
	html = getHTML("http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_India")
	wikitables = getWikitables(html)
	cities = []	
	for wikitable in wikitables:
	    rows = wikitable.find_all('tr')
	    for row in rows:
		    anchors = row.find_all('a')
		    if(len(anchors)==2):
		    	city = anchors[0]['title']
		    	state = anchors[1]['title']
		    	cities.append({'city':city,'state':state})
	sql = createSQL(cities)
	writeSQL(sql)

if __name__ == '__main__':
	main()