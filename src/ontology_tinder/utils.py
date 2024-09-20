from typing_extensions import List

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