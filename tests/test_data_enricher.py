import unittest
import random
from data_enricher.enricher import Enricher


class TestEnricher(unittest.TestCase):
    def setUp(self):
        self.enricher = Enricher()

    def test_enrich_process(self):
        sample_questions = [] #SampleQuestions.get_list()
        
        question = sample_questions[random.randint(0, len(sample_questions))]
        print(question)
        try:
            completion = self.enricher.process(question)
            self.assertIsNotNone(completion)
        except Exception as e:
            self.fail(f"process raised exception {e} for prompt {question}")