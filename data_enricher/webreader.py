import logging, time
from googlesearch import search
import bs4, requests
import cleantext

class WebReader():
    def __init__(self, enricher, nresults: int):
        self.logger = enricher.logger
        self.nresults = nresults       

    def get_urls(self, queries):
        urls = []
        for query in queries:
            self.logger.info(f"Searching: {query}")
            search_results = search(query, num_results=self.nresults)
            
            for url in search_results:
                urls.append((query, url))
                
            time.sleep(1)
        
        return list(set(urls))
    
    def is_text_content(self, url):
        return 'text' in self.get_content_type(url)

    def get_content_type(self, url): 
        # let's fix this to avoid double requests
        try:
            response = requests.get(url, stream=True)
            return response.headers['Content-Type']
        except Exception as e:
            return str(e)
        
    def get_text_from_url(self, url):
        text = ''
        try: 
            # Make a request
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.content, 'html.parser')

            # Remove unnecessary elements
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            text = soup.getText()

            # clean
            text = cleantext.clean(text, lower=False)

            logging.info(f'Retrieved {len(text)} chars from {url}')
        except:
            logging.warning(f'Error reading {url}, page discarded')
        
        return text