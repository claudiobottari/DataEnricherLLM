import pandas as pd
import os, time, re, traceback

from enricher import Enricher
from llm_api import LLM_API
from sample_questions import SampleQuestions

class Benchmark():
    def __init__(self):
        self.enricher = Enricher()

    def get_enriched_answer(self, question):
        return self.enricher.process(question) 

    def get_baseline_answer(self, question):
        return self.enricher.llm_api.get_completion(question)

    def get_file_path(self, question):
        forbidden_chars = r'[<>:"/\\|?*]'
        file_name = re.sub(forbidden_chars, '', question)
        return f'benchmark_results/{file_name}.txt'
    
    def is_already_done(self, question):
        
        return os.path.exists(self.get_file_path(question))

    def save_file(self, question, baseline, enriched_prompt, enriched):
        with open(self.get_file_path(question), 'w', encoding='utf-8') as f:
            f.write(f'\n\n{"-" * 80}\n'.join([question, baseline, enriched_prompt, enriched]))

    def save_xlsx(self, data):
        # Create DataFrame
        df = pd.DataFrame(data, columns=['question','baseline', 'enriched prompt', 'enriched result'])

        # Save it
        if not os.path.exists('benchmark_results'):
            os.makedirs('benchmark_results')      

        file_path = 'benchmark_results/results.xlsx'

        if os.path.exists(file_path):
            os.remove(file_path)
        df.to_excel(file_path, index=False)

    def test_and_retry_benchmark(self):
        """
        Sinceh theprocess is long and can often fail due to OpenAI unavailability, let's cycle forever in order to complete the benchmark
        """
        while True:
            try:
                self.test_benchmark()
            except Exception as ex:
                traceback.print_exc()
                print('Retrying in 2 minute....')
                time.sleep(120)

    def test_benchmark(self):
        # Collect data
        data = []
        for i, question in enumerate(SampleQuestions.get_list()):
            if self.is_already_done(question):
                # in order to retry we check if the file with the question was already created
                print(f'Skip {question} cause it was already done before!')
            else:
                self.enricher.logger.info(f'{i+1}. {question}')
                
                # read the baseline from calling the LLM with just the question
                baseline = self.get_baseline_answer(question)
                self.enricher.logger.info(f'{i+1}. BASELINE: {baseline}')

                # call the enrichemetn process
                enriched, enriched_prompt = self.get_enriched_answer(question)
                self.enricher.logger.info(f'{i+1}. ENRICHED: {enriched}')
                
                # create the dataset
                data_row = (question, baseline, enriched_prompt, enriched)
                data.append(data_row)

                # save results to files
                self.save_file(question, baseline, enriched_prompt, enriched)
                self.save_xlsx(data)

                # let's wait 2 minute to not add up too many requests to openAI
                time.sleep(120)

if __name__ == '__main__':
    Benchmark().test_benchmark()
