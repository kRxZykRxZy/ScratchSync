def connect_session(username, password, *, timeout=10) -> Session:
    # Post request to login API:
    _headers = headers.copy()
    _headers["Cookie"] = "scratchcsrftoken=a;scratchlanguage=en;"
    request = requests.post(
        "https://scratch.mit.edu/login/", json={"username": username, "password": password}, headers=_headers,

        timeout=timeout, errorhandling = False
    )
    try:
        session_id = str(re.search('"(.*)"', request.headers["Set-Cookie"]).group())
    except (AttributeError, Exception):
        raise exceptions.LoginFailure(
            "Either the provided authentication data is wrong or your network is banned from Scratch.\n\nIf you're using an online IDE (like replit.com) Scratch possibly banned its IP adress.")

def get_cloud
