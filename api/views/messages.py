import web
import urllib
from api.utils import api_response, save_api_request
from api.views.base import BaseAPI
from api.views import authentication, tokenManager
from httplib import BadStatusLine, HTTPConnection, HTTPException, HTTPSConnection, IncompleteRead, NotConnected
from mypinnings.auth import authenticate_user_email, force_login, logged_in, \
    authenticate_user_username, login_user, username_exists, email_exists, \
    logout_user, generate_salt, user_id_by_email

from mypinnings.database import connect_db

db = connect_db()

class Messages(BaseAPI):
    """Sharing messages base class, contains two main methods get to list all messages and post to fire message"""
    
    def GET(self):
        """
            List all messages belong to current user.
        """
        try:            
            # check user have access token and token is live
            request = web.input()
            tokenlife = tokenManager.tokenManager().token_check_expire(request.token, request.email.lower())
            if ( tokenlife ):
                user_id = user_id_by_email(request.email.lower())
                print user_id
                message_list = db.select('messages', where="message_to=$id", order="timestamp DESC", vars={'id':user_id}) # db query prevent sql injections
                data = message_list.list()
                response = api_response(data)
                return response
            else:
                return api_response('Invalid token', 200, 403, 'Check your username or password !')
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
            
    def POST(self):
        """
            Fire message to follower [ member ]
        """
        try:
            request = web.input()
            tokenlife = tokenManager.tokenManager().token_check_expire(request.token, request.email.lower())
            # check user have access token and token is live
            if ( tokenlife ): 
                request_data = web.input('message_to', 'sender', 'content', 'email', 'convo_id')
                message = db.insert('messages', convo_id=request_data.convo_id, sender=request_data.sender,content=request_data.content,message_to=request_data.message_to,)#,date=web.SQLLiteral("NOW()"))
                try:
                    if message:
                        response = api_response({'success':True})
                        return response
                    else:
                        response = api_response({'error':True})
                        return response
                except Exception as ex:
                    response = api_response('Exception occured: ' + str(ex), 200, 503, 'Database connection error !')
                    return response                    
            else:
                return api_response('Invalid token', 200, 403, 'Check your username or password !')
            
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
