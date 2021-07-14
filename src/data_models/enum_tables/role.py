# A mapping from role code to role name
ROLE = {
    0: "UNKNOWN_OR_USER",
    1: "Admin",
    2: "SuperAdmin",
}


def from_code_to_role_name(role_code):
    """Return the corresponding name of role.

    Args:
        int, the code of role
    Returns:
        str, the name of role
    """
    if role_code not in ROLE:
        return "UNKNOWN_OR_USER"
    return ROLE[role_code]
