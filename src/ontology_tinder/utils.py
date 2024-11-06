import os

import tqdm
from typing_extensions import List, Tuple

def read_object_names(file_name : str, foulder: str) -> List[str]:
    """
    Reads names and returns them from a given file.

    :param file_name: The name of the file to read.
    :param foulder: The name of the foulder to read.
    :return: A list of names.
    """
    words = []
    with open(os.path.join("..", f"{foulder}", f"{file_name}"), "r") as file:
        words = file.read().split("\n")

    return words

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