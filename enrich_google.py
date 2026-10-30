"""Optional: fetch extra product images/snippets via Google Programmable Search (Custom Search JSON API).
Needs API_KEY and CSE_ID (https://programmablesearchengine.google.com). Do NOT scrape google.com result pages.
Run:  python enrich_google.py products.json  -> writes products_enriched.json with `web` links per product.
Check each brand's licence before reusing their photos commercially."""
import json,sys,urllib.parse,urllib.request
API_KEY='YOUR_API_KEY';CSE_ID='YOUR_CSE_ID'
def search(q,image=False):
    p={'key':API_KEY,'cx':CSE_ID,'q':q,'num':3}
    if image:p['searchType']='image'
    with urllib.request.urlopen('https://www.googleapis.com/customsearch/v1?'+urllib.parse.urlencode(p)) as r:return json.load(r).get('items',[])
d=json.load(open(sys.argv[1]))
for p in d['products']:
    q=f"{p['brand']} {p['name']}"
    p['web']={'images':[i['link'] for i in search(q,True)],'pages':[{'title':i['title'],'url':i['link'],'snippet':i.get('snippet','')} for i in search(q)]}
json.dump(d,open('products_enriched.json','w'),ensure_ascii=False)
