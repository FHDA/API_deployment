# A mapping from degree type code to degree type name.
DEGREE_TYPE = {
    # Todo: Add degree types here.
    0: "UNKNOWN",
    1: "Associate",
    2: "Bachelor",
    3: "Master",
    4: "Ph.D.",
    6: "Certification",
    7: "Joint Degrees",
    8: "Professional",
}


def from_code_to_degree_type_name(degree_type_code):
    """Return the corresponding name of degree type.

    Args:
        int, the code of degree type
    Returns:
        str, the name of degree type
    """
    if degree_type_code not in DEGREE_TYPE:
        return "UNKNOWN"
    return DEGREE_TYPE[degree_type_code]
