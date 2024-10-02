import gensim.downloader as api
import json
from collections import deque

import typing_extensions

test = ("A-Frameshelf",
"AgentBody",
"AlarmClock",
"AluminumFoil",
"AppleA",
"AppleB",
"Armchair",
"Baseballbat")

def load_availables_models():
    """
    Loads every currently available models present in gensim.

    """
    info = api.info()
    models = []
    for model_name, model_data in sorted(info['models'].items()):
        models.append(api.load(model_name))
        print(
            '%s (%d records): %s' % (
                model_name,
                model_data.get('num_records', -1),
                model_data['description'][:40] + '...',
            )
        )
    return models


load_availables_models()

