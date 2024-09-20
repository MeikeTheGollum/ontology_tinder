import os
from ontology_tinder.utils import prune_object_names

def prune_names():
    """
    Read all names from names.txt, prune them and write them to pruned_names.txt
    """
    with open(os.path.join("..", "resources", "names.txt"), "r") as file:
        names = file.read().split("\n")

    pruned_names = prune_object_names(names)
    pruned_names = list(sorted(set(pruned_names)))

    with open(os.path.join("..", "resources", "pruned_names.txt"), "w") as file:
        file.write("\n".join(pruned_names))


if __name__ == "__main__":
    prune_names()