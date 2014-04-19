import web
import urllib
from api.utils import api_response, save_api_request
from api.views.base import BaseAPI
from api.views import authentication
import json
from httplib import BadStatusLine, HTTPConnection, HTTPException, HTTPSConnection, IncompleteRead, NotConnected
from mypinnings.auth import authenticate_user_email, force_login, logged_in, \
    authenticate_user_username, login_user, username_exists, email_exists, \
    logout_user, generate_salt, user_id_by_email

from mypinnings.database import connect_db

db = connect_db()

class tokenManager(BaseAPI):
    """Token manager base class"""
    
    def POST(self):
        try:
            # check user have access token
            request = web.input()
            response = authentication.Auth().GET()
            user_id = authenticate_user_email(request.email.lower(), request.password)
            if not user_id:
                user_id = authenticate_user_username(request.email.lower(), request.password)
            return response
        # Handle exceptions with care       
        except HTTPException as ex:
            response = api_response('HTTPException occured: ' + str(ex), 200, 500, 'Bad Request !')
            return response
        except Exception as ex:
            if ex.args == ("timed out",):
                response = api_response('Exception occured: ' + str(ex), 200, 504, 'Check Internet Connection or refresh token !')
                return response
            else:
                response = api_response('Exception occured: ' + str(ex), 200, 504, 'Access Token Null !')
                return response
            return str(ex)
        pass
    
    def refreshToken(self):
        # refresh user logintoken if expires
        return True
    
    # check if user has token if he entered correct email and password 
    def token_check_expire(self, token, email):
        token = db.select('users', where="logintoken=$token AND email=$email", vars={'email':email,'token':token}) # db query prevent sql injections
        # check if token didn't expired
        if token: 
            return True
        return False
