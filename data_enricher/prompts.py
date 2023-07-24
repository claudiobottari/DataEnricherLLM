class Prompts():
    @staticmethod
    def get_queries_prompt(question: str, nsearches: int) -> str:
        return f'''Please provide a max {nsearches} web search queries that can help to answer this question: "{question}".
Format the result in JSON following this template:
{{
"queries": [...]
}}
'''
    @staticmethod
    def get_information_prompt(content = '', question = ''):
        return f'''
Considering the web page text between triple ``` as the source, 
extract and summarize all information that can be used on answering the question "{question}".

```{content}```
'''
    
    @staticmethod
    def get_rank_information_prompt(infos, question):
        return f'''
Given the text between triple ``` as the source 
and the question "{question}", 
please evaluate and provide a ranking on a scale from 1 to 100, 
with 1 indicating no relevance and 10 indicating high relevance, 
on how well the text answers the question.

```{infos}```

Format the result in JSON following this template:
{{
"rank": ...
}}
'''
    
    @staticmethod
    def get_prompted_infos(url, text):
        return f'''
<START>
[{url}]
{text}
<END>
'''
    @staticmethod
    def get_enriched_prompt(question):
        return f'''
In the context of the information delimited by <START> and <END> tags, please answer the subsequent question.
Be as clear and specific as possible, making use of all provided details.
If you use any information delimited by <START> and <END> tags, please cite the source url which is written between brackets.

Question: {question}

Information:'''