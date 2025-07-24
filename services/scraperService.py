import json
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import re

class ScraperService:
    def __init__(self, sources_path='sources.json'):
        self.sources_path = sources_path
        self.sources = self.load_sources()

    def load_sources(self) -> List[str]:
        try:
            with open(self.sources_path, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def get_news(self, topic: str) -> List[Dict]:
        if not self.sources:
            return []
        results = []
        exact_topic = f'"{topic}"'
        intitle_topic = f'intitle:{exact_topic}'
        # Buscar en fuentes confiables
        for source_url in self.sources:
            domain = source_url.replace('https://', '').replace('http://', '').split('/')[0]
            query = f'{intitle_topic} site:{domain} when:7d'
            url = f'https://news.google.com/search?q={requests.utils.quote(query)}&hl=es-419&gl=ES&ceid=ES%3Aes'
            try:
                resp = requests.get(url, timeout=8)
                soup = BeautifulSoup(resp.text, 'html.parser')
                articles = soup.select('article')
                for art in articles:
                    title_tag = art.find('h3') or art.find('h4')
                    link_tag = art.find('a', href=True)
                    if title_tag and link_tag:
                        title = title_tag.text.strip()
                        href = link_tag['href']
                        if href.startswith('./'):
                            href = 'https://news.google.com' + href[1:]
                        results.append({
                            "valor": title,
                            "path": href
                        })
                        if len(results) >= 3:
                            return results
            except Exception:
                continue
        # Si no se encontró nada, hacer una búsqueda general en Google News
        if not results or len(results) < 3:
            query = f'{intitle_topic} when:7d'
            url = f'https://news.google.com/search?q={requests.utils.quote(query)}&hl=es-419&gl=ES&ceid=ES%3Aes'
            temp_results = []
            try:
                resp = requests.get(url, timeout=8)
                soup = BeautifulSoup(resp.text, 'html.parser')
                articles = soup.select('article')
                for art in articles:
                    title_tag = art.find('h3') or art.find('h4')
                    link_tag = art.find('a', href=True)
                    if title_tag and link_tag:
                        title = title_tag.text.strip()
                        href = link_tag['href']
                        if href.startswith('./'):
                            href = 'https://news.google.com' + href[1:]
                        temp_results.append({
                            "valor": title,
                            "path": href
                        })
                        if len(temp_results) >= 3:
                            break
            except Exception:
                pass
            if len(temp_results) == 3:
                return temp_results
            else:
                return []
        return results

    def get_image(self, topic: str) -> str:
        if not self.sources:
            return ""
        # Busca una imagen relevante en Wikipedia
        try:
            search_url = f"https://es.wikipedia.org/wiki/{requests.utils.quote(topic.replace(' ', '_'))}"
            resp = requests.get(search_url, timeout=8)
            soup = BeautifulSoup(resp.text, 'html.parser')
            infobox = soup.find('table', class_='infobox')
            if infobox:
                img = infobox.find('img')
                if img and img['src']:
                    return 'https:' + img['src']
            img = soup.find('img')
            if img and img['src']:
                return 'https:' + img['src']
            return ""
        except Exception:
            return "" 