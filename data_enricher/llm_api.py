import os
import openai
import spacy
import tiktoken
from datetime import datetime

from prompts import Prompts

TOKEN_RESPONSE_BUFFER = 600
MAX_MODEL_TOKENS = 4096 - TOKEN_RESPONSE_BUFFER # not tested, but it should be the actual max token number for gpt 3.5

class LLM_API:
    def __init__(self, enricher):
        self.logger = enricher.logger
        self.api_key = self.get_api_key()
        self.model = "gpt-3.5-turbo"
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.nlp = spacy.load('en_core_web_sm')

        if self.api_key is None:
            self.logger.error("API key is not set.")
        else:
            openai.api_key = self.api_key

    @staticmethod
    def get_api_key():
        """
        Retrieve the OpenAI API key from environment variables.
        """
        return os.getenv("OPENAI_API_KEY")

    def num_tokens_from_string(self, string: str) -> int:
        """
        Retrieve the number of token for the current encoding of the specified string
        """
        return len(self.encoding.encode(string))

    def save_llm_interaction(self, timestamp, label, body):
        formatted_timestamp = timestamp.strftime('%Y%m%d%H%M%S%f')

        with open(f'llm/{formatted_timestamp}.{label}', 'w', encoding='utf-8') as f:
            f.write(str(body))

    def get_completion(self, prompt, temperature=0.5):
        """
        Use the OpenAI API to get a completion for the provided prompt.

        :param prompt: The prompt to complete.
        :param tokens: The maximum number of tokens in the generated output. (default: 100)
        :param temperature: The creativity of the output. Higher values generate more random outputs. (default: 0.5)
        :return: The generated completion.
        """
        if self.api_key is None:
            self.logger.error("Cannot get completion, API key is not set.")
            return None

        timestamp = datetime.now()
        messages = [{"role": "user", "content": prompt}]
        self.save_llm_interaction(timestamp, 'prompt', prompt)

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        self.save_llm_interaction(timestamp, 'completion', response.choices[0].message["content"])
        
        return response.choices[0].message["content"]
    
    def get_chunks(self, content):
        pars = self.split_text_spacy(content)
        prompt_delta = self.num_tokens_from_string(Prompts().get_information_prompt()) + 1
        buffer = '\n'
        for par in pars:
            if self.num_tokens_from_string(buffer + '\n' + par) + prompt_delta > MAX_MODEL_TOKENS:
                yield buffer
                buffer = '' 
            
            buffer += '\n' + par
        
        yield buffer

    def split_text_spacy(self, text):
        # load doc with spacy
        doc = self.nlp(text)
        # return list of paragraphs using spacy capabilities
        return [sent.text.strip() for sent in doc.sents]
    
    def does_prompt_exceeds_maxtokens(self, prompt):
        """
        Check if the specified prompt exceed the max context for th current model
        """
        num_tokens = self.num_tokens_from_string(prompt)
        return num_tokens > MAX_MODEL_TOKENS
