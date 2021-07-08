# A mapping from school code to school name.
SCHOOL = {
    # Todo: Add school names here.
    0: "UNKNOWN",
    1: "University of California, Berkeley",
    2: "University of California, Los Angeles",
    3: "University of California, San Diego",
    4: "University of California, Santa Barbara",
    5: "University of California, Irvine",
    6: "University of California, Davis",
    7: "University of California, Riverside",
    8: "University of California, Merced",
    9: "University of California, San Francisco",
    10: "De Anza College",
}


def from_code_to_school_name(school_code):
    """Return the corresponding name of school.

    Args:
        int, the code of school
    Returns:
        str, the name of school
    """
    if school_code not in SCHOOL:
        return "UNKNOWN"
    return SCHOOL[school_code]
