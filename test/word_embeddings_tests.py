import unittest

from src.ontology_tinder import word_embeddings

class Word_Embeddings(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_getSimilarity(self):
        self.assertEqual(word_embeddings.getSimilarity('alarmclock_1', 'alarmclock_1'), 1.0)
    def test_error(self):
        self.ass
if __name__ == '__main__':
    unittest.main()
