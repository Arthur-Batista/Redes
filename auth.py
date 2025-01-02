def authenticate(credentials, user_credentials):
    try:
        username, password = credentials.split(":")
        if username in user_credentials and user_credentials[username] == password:
            return True, username
        return False, None
    except ValueError:
        return False, None
    
    