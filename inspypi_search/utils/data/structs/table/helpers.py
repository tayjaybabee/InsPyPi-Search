def sanitize_header(header):
    """
    Return the provided string after converting it to lower-case and then replacing all whitespace with '_'

    Args:
        header:
            The string you want sanitized.

    Returns:
        str
    """
    return header.lower().replace(' ', '_')
