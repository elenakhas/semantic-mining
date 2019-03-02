from typing import Dict

from word_tree import Primitive


def get_primitives_dict() -> Dict[str, Primitive]:
    """
    Create a dictionary of all the primitives described in
    https://intranet.secure.griffith.edu.au/schools-departments/natural-semantic-metalanguage/in-brief

    :return: a dictionary pf the primitives, with the key beeing the string representation of the primitive and the
    value being the corresponding Primitive object
    """

    primitives_class_str = {
        "Substantives": {"I", "YOU", "SOMEONE", "PERSON", "PEOPLE", "SOMETHING", "THING", "BODY"},
        "Relational substantives": {"KIND", "PART"},
        "Determiners": {"THIS", "THE SAME", "OTHER", "ELSE", "ANOTHER"},
        "Quantifiers": {"ONE", "TWO", "SOME", "ALL", "MUCH", "MANY", "LITTLE", "FEW"},
        "Evaluators": {"GOOD", "BAD"},
        "Descriptors": {"BIG", "SMALL"},
        "Mental predicates": {"THINK", "KNOW", "WANT", "FEEL", "SEE", "HEAR"},
        "Speech": {"SAY", "WORDS", "TRUE"},
        "Actions, events, movement, contact": {"DO", "HAPPEN", "MOVE", "TOUCH"},
        "Location, existence, possession, specification": {"BE", "SOMEWHERE", "THERE IS", "HAVE", "BE", "SOMEONE",
                                                           "SOMETHING"},
        "Life and death": {"LIVE", "DIE"},
        "Time": {"WHEN", "TIME", "NOW", "BEFORE", "AFTER", "A LONG TIME", "A SHORT TIME", "FOR SOME TIME", "MOMENT"},
        "Space": {"WHERE", "PLACE", "HERE", "ABOVE", "BELOW", "FAR", "NEAR", "SIDE", "INSIDE"},
        "Logical concepts": {"NOT", "MAYBE", "CAN", "BECAUSE", "IF"},
        "Intensifier, augmentor": {"VERY", "MORE"},
        "Similarity": {"LIKE", "AS", "WAY"},
    }

    # Flatten the dictionary as a set, to make it usable as a filter
    primitives_str = set()
    for primitive_class in primitives_class_str.values():
        primitives_str |= {primitive_str.lower() for primitive_str in primitive_class}

    # Build all the Primitive objects from the set
    primitives = {primitive: Primitive(primitive) for primitive in primitives_str}

    return primitives


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_primitives_dict())
