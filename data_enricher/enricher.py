from llm_api import LLM_API
from prompts import Prompts
from webreader import WebReader

import json
import pyperclip
import logging

DEFAULT_NSEARCHES = 3
DEFAULT_NRESULTS = 5

class Enricher:
    def __init__(self, nsearches: int = DEFAULT_NSEARCHES, nresults: int = DEFAULT_NRESULTS, verbose: bool = False, clipboard: bool = False):
        verbose = True
        # Set up logging
        self.logger = logging.getLogger('Enricher')
        self.logger.level=logging.DEBUG if verbose else logging.WARNING
        self.logger.format="%(asctime)s [%(levelname)s] %(message)s"
        self.logger.handlers=[
                logging.StreamHandler(),  # Output to console
                logging.FileHandler('data_enricher.log', mode='w')
            ]
        # Set up internal objs
        self.llm_api = LLM_API(self)
        self.webreader = WebReader(self, nresults)
        self.nsearchs = nsearches
        self.clipboard = clipboard

    def get_queries(self, question):
        # get prompt and ask llm
        prompt = Prompts().get_queries_prompt(question, self.nsearchs)
        json_queries = self.llm_api.get_completion(prompt)
        
        # parse result
        data = json.loads(json_queries)
        queries = data["queries"]

        # log and return list
        self.logger.info(f'Retrieved these {len(queries)} queries: ' + ', '.join(queries))
        return queries

    def rank_information(self, infos, question):
        prompt = Prompts().get_rank_information_prompt(infos, question)   
        completion = self.llm_api.get_completion(prompt)
        
        json_completion = json.loads(completion)  
        return json_completion['rank']

    def get_information(self, content, query, question):
        prompt = Prompts().get_information_prompt(content, question)  
        return self.llm_api.get_completion(prompt)
    
    def get_summary(self, topic, content):
        prompt = Prompts().get_summary_prompt(topic, content)
        completion = self.llm_api.get_completion(prompt)
        data = json.loads(completion)
        
        return data['relevance'], data['informations']
        
    def get_data(self, question, all_urls):
        data = []
        for query, url in all_urls:
            self.logger.info(f'Reading {url} related to {query}')
            if self.webreader.is_text_content(url):
                content = self.webreader.get_text_from_url(url)
                chunks = self.llm_api.get_chunks(content)
                for chunk in chunks:
                    infos = self.get_information(chunk, query, question)
                    rank = self.rank_information(infos, question)
                    data.append((rank, query, url, infos))    
            else:
                self.logger.info(f'skip {url}')

        self.logger.info(f'Found {len(data)} infos')

        # cut infos not really relevant
        # NOTE: may be significant to tune that 50%
        data = [infos for infos in data if infos[0] > 50]
        self.logger.info(f'Selected {len(data)} infos')

        # return sorted by relevance
        return sorted(data, key=lambda x: x[0], reverse=True)
        
    def process(self, question: str) -> str:
        self.logger.info(f"Starting the Enricher, question: {question}")
        
        # find the list of google queries that should be performed in order to find relevant informations
        queries = self.get_queries(question)
        
        # collect of the urls that should be scraped for content
        urls = self.webreader.get_urls(queries)

        # read the data from the url and collect it in a smart way
        data = self.get_data(question, urls)

        # enrich the prompt adding data in order of descending importance and minding 
        # to not exceed the max number of token allowed by the LLM
        prompt = Prompts().get_enriched_prompt(question)
        enriched_prompt = prompt
        for d in data:
            prompt += Prompts().get_prompted_infos(d[2], d[3])
            if self.llm_api.does_prompt_exceeds_maxtokens(prompt):
                break
            enriched_prompt = prompt

        # copy the final prompt it on the clipboard if requested
        if self.clipboard:
            pyperclip.copy(enriched_prompt)

        # finally return the LLM output from the enriched prompt
        return self.llm_api.get_completion(enriched_prompt)
