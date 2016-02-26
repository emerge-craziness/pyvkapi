import requests, re, json
from urllib.parse import urlparse, parse_qsl, urlencode
from sys import stderr
from datetime import datetime

LOGGING = True

def log( *msgs, end = "\n", sep = " ", flush = True ):
    if LOGGING:
        stderr.write( sep.join( ( str( msg ) if type( msg ) is not dict else json.dumps( msg, ensure_ascii = False, indent = 4 ) ) for msg in msgs ) + end )
        if flush: stderr.flush()

class VkApiException( Exception ):
    pass

class IntermediateApiMethodsClass:
    pass

class VkApi:
    def __init__( self, **kwargs ):
        self.s = requests.Session()
        self.s.headers['Accept'] = 'application/json'
        self.s.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        self.V = 5.45
        self.LANG = kwargs.pop( 'lang', 'ru' )
        self.SCOPE = kwargs.pop( 'scope', 'wall,messages,friends,audio' )
        self.APP_ID = kwargs.pop( 'app_id', 3682744 )
        self.LOGIN = kwargs.pop( 'login', None )
        self.LOGIN = kwargs.pop( 'email', self.LOGIN )
        self.PASSWORD = kwargs.pop( 'password', None )

        self.ACCESS_TOKEN = kwargs.pop( 'access_token', None )
        if self.ACCESS_TOKEN:
            self.token_expires_in = 60
            self.token_birth = datetime.now()

        def callable_method( self, method_name ):
            def method( **params ):
                return self.__parse_response( self.__call_method( method_name, params ) )
            return method

        from methods import methods
        for higher in methods:
            self.__setattr__( higher, IntermediateApiMethodsClass() )
            for lower in methods[higher]:
                self.__getattribute__( higher ).__setattr__( lower, callable_method( self, "%s.%s" % ( higher, lower ) ) )

    def get_new_access_token( self ):
        LOGIN_URL = 'https://m.vk.com'
        AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
        CAPTCHA_URI = 'https://m.vk.com/captcha.php'

        TIMEOUT = 0.1 # seconds

        if None in ( self.LOGIN, self.PASSWORD ):
            self.ACCESS_TOKEN = ""
            self.token_birth = datetime.now()
            self.token_expires_in = 0
            return ""

        def get_form_action( html ):
            form_action = re.findall( '<form(?= ).* action="(.+)"', html )
            if form_action:
                return form_action[0]

        def login():
            response = self.s.get( LOGIN_URL )
            login_form_action = get_form_action( response.text )
            if not login_form_action:
                raise Exception('VK changed login flow')

            login_form_data = { 
                "email": self.LOGIN,
                "pass": self.PASSWORD
            }
            
            response = self.s.post( login_form_action, login_form_data )
            response_url_query = get_url_query( response.url )

            if 'remixsid' in self.s.cookies or 'remixsid6' in self.s.cookies:
                return

            if 'sid' in response_url_query:
                raise Exception( "auth_captcha_is_needed: %s : %s" % (response, login_form_data) )
            elif response_url_query.get('act') == 'authcheck':
                raise Exception( "auth_check_is_needed: %s" % (response.text) )
            elif 'security_check' in response_url_query:
                raise Exception( "phone_number_is_needed: %s" % ( response.text ) )
            else:
                raise Exception( 'Authorization error (incorrect password)' )
        
            return oauth2_authorization()['access_token']

        def oauth2_authorization():
            auth_data = {
                'client_id': self.APP_ID,
                'display': 'mobile',
                'response_type': 'token',
                'scope': self.SCOPE,
                'v': self.V,
                'lang': self.LANG
            }
            response = self.s.post( AUTHORIZE_URL, auth_data, timeout = TIMEOUT )
            response_url_query = get_url_query( response.url )
            if 'access_token' in response_url_query:
                return response_url_query
            
            form_action = get_form_action( response.text )
            if form_action:
                response = self.s.get( form_action, timeout = TIMEOUT )
                response_url_query = get_url_query( response.url )
                return response_url_query

            try: response_json = response.json()
            except ValueError:  error_message = 'OAuth2 grant access error'
            else: error_message = 'VK error: [{}] {}'.format(response_json['error'], response_json['error_description'])
            raise Exception(error_message)

        def get_url_query( url ):
            parsed_url = urlparse( url )
            url_query = parse_qsl( parsed_url.fragment )
            url_query = dict( url_query )
            return url_query

        login()
        auth_response_url_query = oauth2_authorization()
        
        log( auth_response_url_query )
        if 'access_token' in auth_response_url_query:
            self.token_birth = datetime.now()
            self.ACCESS_TOKEN = auth_response_url_query['access_token']
            self.token_expires_in = auth_response_url_query['expires_in']
            return auth_response_url_query['access_token']
        else:
            raise VkApiException( 'OAuth2 authorization error' ) 

    def __call_method( self, name, params ):
        if self.ACCESS_TOKEN is None or (datetime.now() - self.token_birth).total_seconds() > int( self.token_expires_in ):
            self.get_new_access_token()

        timeout = params.pop( "timeout", 2 )
        for param in ( 'lang', 'access_token', 'v' ):
            if param not in params:
                params[param] = self.__getattribute__( param.upper() )
        BASE_URL = "https://api.vk.com/method"
        params_string = ""
        for key, value in params.items():
            params_string += "%s=%s&" % ( key, value )
            
        url = BASE_URL + ("/%s?" % name) + params_string
        log( "trying to get '%s'" % url )
        try: return self.s.get( url, timeout = timeout ).json()
        except Exception as e: log( "Catched an error: %s" % e )

    def __parse_response( self, response ):
        # TODO check answer
        return response

if __name__ == "__main__":
    api = VkApi( login = None, password = None )
    print( api.users.get( user_id = 1 ) )

    # To call this, setup login and password first
    # print( json.dumps( api.messages.get(), indent = 4, ensure_ascii = False ) ) 

