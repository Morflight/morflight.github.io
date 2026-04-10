serve:
	python3 -m http.server 8080

smoke:
	@python3 -c "from html.parser import HTMLParser; [HTMLParser().feed(open(f).read()) for f in ['index.html','about.html','community.html','contact.html','streamers.html']]" && echo "smoke: html parse ok" || (echo "smoke: html parse fail" && exit 1)
