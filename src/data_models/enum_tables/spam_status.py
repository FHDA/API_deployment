# A mapping from spam status code to spam status
SPAM_STATUS = {
    0: "UNKNOWN",
    1: "PendingSpam",
    2: "ConfirmedSpam",
    3: "ConfirmedNoSpam",
}


def from_code_to_spam_status(spam_status_code):
    """Return the corresponding spam status.

    Args:
        int, the code of spam status
    Returns:
        str, the name of spam status
    """
    if spam_status_code not in SPAM_STATUS:
        return "UNKNOWN"
    return SPAM_STATUS[spam_status_code]
