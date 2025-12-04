import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import json

def extractLinks(soup):
    links = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        if not url.startswith("http"):
            url = "https://en.wikipedia.org" + url
        links.append(url)
    return links

def extractImages(soup):
    images = []
    for img in soup.find_all("img", src=True):
        url = img["src"]
        if not url.startswith("http"):
            url = "https://en.wikipedia.org" + url
        if "static/images" not in url:
            images.append(url)
    return images

def extractTables(soup):
    tables = []
    for t in soup.find_all("table", {"class": "wikitable"}):
        thtml = StringIO(str(t))
        df = pd.read_html(thtml)[0]
        tables.append(df)
    return tables

def extractParagraphs(soup):
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    return [p for p in paragraphs if p and len(p) > 10]

def saveData(term, links, images, tables, paragraphs):
    with open(term + "_links.txt", "w", encoding="utf-8") as f:
        for link in links:
            f.write(f"{link}\n")

    with open(term + "_images.json", "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4)

    with open(term + "_paragraphs.txt", "w", encoding="utf-8") as f:
        for p in paragraphs:
            f.write(f"{p}\n\n")
    
    for i, table in enumerate(tables):
        table.to_csv(term + f"_{i+1}.csv", index=False, encoding="utf-8-sig")

def scrapeWikipedia(url, keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = extractLinks(soup)
    images = extractImages(soup)
    tables = extractTables(soup)
    paragraphs = extractParagraphs(soup)

    saveData(keyword, links, images, tables, paragraphs)

if __name__ == "__main__":
    #scrapeWikipedia("https://en.wikipedia.org/wiki/Cristiano_Ronaldo", "CRonaldo")
    #scrapeWikipedia("https://en.wikipedia.org/wiki/LangChain", "LangChain")
    scrapeWikipedia("https://en.wikipedia.org/wiki/Python_(programming_language)", "Python")
 