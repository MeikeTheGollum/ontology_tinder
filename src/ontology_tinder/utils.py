import tqdm
from gensim.models import Word2Vec, KeyedVectors
from typing_extensions import List, Tuple


def prune_object_names(object_names: List[str]) -> List[str]:
    """
    Prune object names to remove the suffixes

    Example:
    >>> object_names = ["alarmclock_1", "agentbody_1", "alarmclock_2"]
    >>> prune_object_names(object_names)
    ["alarmclock", "agentbody", "alarmclock"]

    :param object_names: The list of object names
    :return: The pruned object names
    """
    return [name.split("_")[0] for name in object_names]


def model_coverage_of_words(model: KeyedVectors, names: List[str]) -> Tuple[List[str], List[str]]:
    """
    Get the words that are contained in the model and the words that are not contained in the model

    :param model: The model
    :param names: The names
    :return: The contained names and the not contained names
    """

    contained_names = []
    not_contained_names = []
    for item in tqdm.tqdm(names, desc="Checking model coverage"):
        try:
            model.__getitem__(item)
        except KeyError as e:
            not_contained_names.append(item)
        else:
            contained_names.append(item)
    return contained_names, not_contained_names

def direct_match_coverage_of_words(concepts:List[str], names:List[str]) -> Tuple[List[str], List[str]]:
    contained_names = []
    not_contained_names = []
    for item in tqdm.tqdm(names, desc="Checking direct match coverage"):
        try:
            tmp = concepts.index(item)
        except ValueError:
            not_contained_names.append(item)
        else:
            contained_names.append(item)
    return  contained_names, not_contained_names