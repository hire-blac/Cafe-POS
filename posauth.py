AUTH_TOKEN ='authtokenabc'

def Auth(request):
    username =  request.get_cookie('user_name')
    return request.get_cookie('auth_token') == AUTH_TOKEN + username

def GetAuthToken(username):
    return AUTH_TOKEN + username

def isAdmin(request):
    user_type =  request.get_cookie('user_type')
    return user_type == 'Administrator'