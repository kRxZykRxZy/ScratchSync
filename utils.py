# utils.py

import re

def extract_csrf_token(html_content):
    match = re.search(r'csrf_token" value="([^"]+)', html_content)
    if match:
        return match.group(1)
    return ''
