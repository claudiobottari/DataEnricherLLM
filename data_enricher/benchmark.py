import pandas as pd
import os

from enricher import Enricher
from llm_api import LLM_API
from sample_questions import SampleQuestions

class Benchmark():
    def __init__(self):
        self.enricher = Enricher()
        self.llm_api = LLM_API()

    def get_enriched_answer(self, question):
        return self.enricher.process(question) 

    def get_baseline_answer(self, question):
        return self.llm_api.get_completion(question)

    def test_benchmark(self):
        # Collect data
        data = []
        for question in SampleQuestions.get_list():
            print(question)
            baseline = self.get_baseline_answer(question)
            print(baseline)
            enriched = self.get_baseline_answer(question)
            print(enriched)
            data.append((baseline, enriched))
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=['baseline', 'enriched'])

        # Save it
        if not os.path.exists('benchmark_results'):
            os.makedirs('benchmark_results')       
        df.to_excel('benchmark_results/results.xlsx', index=False)

if __name__ == '__main__':
    Benchmark().test_benchmark()
