import urllib.request# import urlopen
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup as bs

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]


def search(query):
	google_path = "http://images.google.com/searchbyimage?image_url=https://i.ytimg.com/vi/LT7lSw3leV0/maxresdefault.jpg"
	source_code = opener.open(google_path).read()
	# print (source_code)
	source_code = source_code.decode("utf8")
	soup = bs(source_code,'lxml')
	tags = soup.findAll("div",{"class" : "rc"})
	related_search_tag = soup.find('a',{"class" : "fKDtNb"})
	if related_search_tag:
		related_search = related_search_tag.contents[0]
		print ("Related Search : {}".format(related_search))
	search_results = []
	for tag in tags:
		search_results.append([tag.find("h3").text, tag.find("div",{"class" : "s"}).text, tag.find('a').get('href')])
	# rank = []
	i = 0
	for search_result in search_results:
		cnt = 0
		qr = query.split()
		for word in qr:
			print (word)
			cnt += search_result[1].count(word)
		search_results[i].insert(0,cnt)	
		i+=1
	search_results.sort(reverse=True)
	print(search_results) 
search("Who is this person")