# A mapping from major code to major name.
MAJOR = {
    # Todo: Add major lists here.
    0: "UNKNOWN",
    1: "Mathematics",
    2: "Statistics",
    3: "Communication",
    4: "Computer Science",
    6: "Data Science",
}


def from_code_to_major_name(major_code):
    """Return the corresponding name of major.

    Args:
        int, the code of major
    Returns:
        str, the name of major
    """
    if major_code not in MAJOR:
        return "UNKNOWN"
    return MAJOR[major_code]
