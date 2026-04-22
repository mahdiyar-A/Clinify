import re


def normalize_person_name(value: str) -> str:
    """Normalize first/last names for storage.
    """
    if value is None:
        return ''

    value = ' '.join(str(value).strip().split())
    if not value:
        return ''

    value = value.lower()
    parts = re.split(r"([\s\-'])", value)

    out = []
    for part in parts:
        if not part:
            continue
        if part in (' ', '-', "'"):
            out.append(part)
            continue
        out.append(part[0].upper() + part[1:])

    return ''.join(out)

