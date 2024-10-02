import gensim.downloader as api
import json
from collections import deque

import typing_extensions


def load_availables_models():
    """

    """
    info = api.info()
    model1 = api.load("glove-wiki-gigaword-200")
    print(model1.most_similar("cat"))

# def detect_percentage_of_keys_present(model, names: list(str)) -> int:
#     """
#
#     """
#     count = 0
#     final_dict = {x:names[x] for x in names
#                   if x in model}
#     print("final dic:", str(final_dict))
#     return (len(final_dict))
