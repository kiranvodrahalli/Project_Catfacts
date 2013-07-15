# fact_scraper.py
# Kiran Vodrahalli
# last updated: 07/14/2013
# general purpose website scraper
# optimized to work with certain websites listed as special urls below 
# will later be made to work in general, this is a very hacky and unstable version
# USED FOR catfacts.py WHICH SENDS YOU CAT FACTS 

from bs4 import BeautifulSoup
import urllib2
import re

#NOTABLE ISSUE: DOES NOT SUPPORT SOME TYPES OF CHARACTERS 

cat_url = "http://facts.randomhistory.com/interesting-facts-about-cats.html" # WORKS WELL
# produceObjects(html, ['li'], "", [], False, "CAT_FACT")
dog_url = "http://facts.randomhistory.com/2009/02/15_dogs.html" # WORKS WELL
# produceObjects(html, ['li'], "", [], False, "DOG_FACT")
dog_url2 = "http://www.petfinder.com/dogs/bringing-a-dog-home/facts-about-new-dog/" # WORKS WELL
# produceObjects(html, ['p'], "", [], False, "DOG_FACT")
bay_area_url = "http://www.buzzfeed.com/nataliemorin/26-awesome-things-the-bay-area-does-right" # WORKS WELL
# produceObjects(html, ['h2'], "", ["span.buzz_superlist_number_inline"], True, "BAY_AREA_AWESOME_FACT")
mac_url = "http://www.buzzfeed.com/jessicamisener/31-cool-things-to-do-with-the-apple-logo-on-your-mac" #WORKS WELL
# produceObjects(html, ['h2'], "", ["span.buzz_superlist_number_inline"], True, "MAC_BUZZFEED_FACT")
python_url = "http://docs.python.org/2/library/urllib2.html"
# doesn't really work 
summer_url = "http://parentingteens.about.com/od/teenculture/a/funteenstodo.htm" # WORKS WELL 
# produceObjects(urllib2.urlopen(summer_url).read(), ['li'], "", [], False, "SUMMER_FACT")
craigslist_url = "http://sfbay.craigslist.org/bka/" # ISSUE WITH WEBSITE KNOWING IM A BOT
# produceObjects(urllib2.urlopen(req).read(), [], "pen/bks", [], False, "CRAIGSLIST_POST") # note simplicity 
hknews_url = "https://news.ycombinator.com" # WORKS WELL 
# produceObjects(urllib2.urlopen(hknews_url).read(), [], "http://", [], False, "HKNEWS_POST") 


#req = urllib2.Request(craigslist_url)
#req.add_header('User-Agent', "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")

def crawl(url, params):
	req = urllib2.Request(url)
	req.add_header('User-Agent', "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")

	html = urllib2.urlopen(req).read()
	data = {}
	for item in params:
		#"a|class1|class2|,,," = params[item]
		html_class = params[item].split('|')[0]
		classes = params[item].split('|')[1:]
		myhref = 'http://' if (url == hknews_url) else ''
		data[item] = produceObjects(html, html_class, myhref, classes, len(classes) == 0, item)
	return data

def produceObjects(html, html_class, myhref, classes, isCSS, name):
	ans = []
	soup = BeautifulSoup(html)
	sentence = ""
	if myhref is not "":
		links = soup.find_all(href=re.compile(myhref))
		for link in links:
			link = link.encode('utf-8')
			ans.append(link)

	elif isCSS:
		raw_texts = soup(html_class[0])
		for string in raw_texts: 
			string_elem = string.encode('utf-8')
			m = re.findall(r'<[a-zA-Z0-9]*\b[^>]*>(.*)</[a-zA-Z0-9]*>[a-zA-Z0-9]*', string_elem)
			mylist = [x for x in m if not x is '']
			for s in mylist:
				#s.encode('utf-8')
				m2 =  re.findall(r'<[a-zA-Z0-9]*\b[^>]*>(.*)</[a-zA-Z0-9]*> ([.a-zA-Z0-9 %]*)', s)
				mylist2 = [x for x in m2 if not x is '']
				for s2 in mylist2:
					ans.append(s2[0] + " " + s2[1])

	else:
		texts = soup.find_all(html_class[0]) #just html, assuming not css
		for text in texts:
			#for deep_text in text.find_all(demarkers[1]):
			split_texts = re.split('<[a-z/]*>', text.encode('utf-8'))
			for new_text in split_texts:
				m3 = re.findall(r'<?[a-zA-Z0-9./]*>?', new_text)
				mylist = [x for x in m3 if not x is '']
				if (len(mylist) > 0):
					if (mylist[0][:1] is not '<'):
						string = ' '.join(str(item) for item in mylist)
						if string[-1:] is '.':
							sentence += string
							if len(sentence) > 4:
								ans.append(str(sentence))
								sentence = ""
						else:
							if len(string) > 4:
								sentence += string 
	return ans
				