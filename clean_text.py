import re

def clean_id(input_text):
    pattern = re.compile(r"title-[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12} comma1", re.IGNORECASE)
    x = pattern.match(input_text)
    x = x.group()
    x = x.replace("title-", "")
    x = x.replace(" comma1", "")

    return x

