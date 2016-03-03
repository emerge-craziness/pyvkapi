import requests, re, json, time
from urllib.parse import urlparse, parse_qsl, urlencode
from sys import stderr
from datetime import datetime

LOGGING = True

def log( *msgs, end = "\n", sep = " ", flush = True ):
    if LOGGING:
        stderr.write( sep.join( ( str( msg ) if type( msg ) is not dict else json.dumps( msg, ensure_ascii = False, indent = 4 ) ) for msg in msgs ) + end )
        if flush: stderr.flush()

class VkApiException( Exception ):
    def __init__( self, exception ):
        self.code = exception['error_code']
        self.message = exception['error_msg']
        self.request_params = exception['request_params']
    def __str__( self ):
        return "VkApiException #{code}: {msg}. Request parameters: {params}\n".format(
                        code = self.code,
                        msg = self.message,
                        params = json.dumps( self.request_params, indent = 4, ensure_ascii = False )
                )

    def __repr__( self ):
        return self.__str__()

class IntermediateApiMethodsClass:
    pass

def loop_errors_handler( func, timeout = 0.1, number_of_tries = 10 ):
    # TODO move here the ideas from lines 66, 123
    pass

class VkApi:
    def __init__( self, **kwargs ):
        self.s = requests.Session()
        self.s.headers['Accept'] = 'application/json'
        self.s.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        self.V = 5.45
        self.LANG = kwargs.pop( 'lang', 'ru' ).lower()
        self.SCOPE = ''.join( kwargs.pop( 'scope', 'wall,messages,friends,audio' ).split() )
        self.APP_ID = kwargs.pop( 'app_id', 3682744 )
        self.LOGIN = kwargs.pop( 'login', None )
        self.LOGIN = kwargs.pop( 'email', self.LOGIN )
        self.PASSWORD = kwargs.pop( 'password', None )

        # possible modes: input, rucaptcha, lastmessage
        kwargs.pop( 'captcha_mode', 'manual' )
        # TODO implement self.captcha_solver(): and rucaptcha 
        if 'rucaptcha_key' in kwargs:
            from rucaptcha import RUCaptcha
            rucaptcha = RUCaptcha( apikey = kwargs.pop( 'rucaptcha_key' ) )
            # def __rucaptcha_solve( self, image ):
            #   pass
            # self.captcha_solver = __rucaptcha_solve

        # remove any whitespaces
        if self.LOGIN: self.LOGIN = ''.join( self.LOGIN.split() )

        self.ACCESS_TOKEN = kwargs.pop( 'access_token', None )
        if self.ACCESS_TOKEN:
            self.token_expires_in = 60
            self.token_birth = datetime.now()

        def callable_method( self, method_name ):
            def method( **params ):
                for i in range( 2 + params.pop( 'number_of_tries', 10 ) ):
                    if i > 0: log( "method %s iteration %i" % (method_name, i) )
                    try:
                        response = self.__call_method( method_name, params )
                        return self.__parse_response( response )
                    except VkApiException as e:
                        if e.code in (6, 9): 
                            # "too many requests per second"
                            # "too much captcha requests"
                            timeout = params.get( 'timeout', 2 )
                            log( "Sleeping for {s}s due to #{code}: {msg}".format( 
                                s = timeout * (2 + i ** 2),
                                code = e.code,
                                msg = e.message
                             ) )
                            time.sleep( timeout * (2 + i ** 2) )
                        else:
                            raise e
                    except requests.exceptions.ReadTimeout as e:
                        params['timeout'] = params.get( 'timeout', 2 ) * 2
                        log( '%s catched. Increasing timeout 2 times, %ss now' % (e, params['timeout']) )
                    except requests.exceptions.ReadTimeout as e:
                        log( '%s catched. Sleeping for %ss' % (e, timeout * (2 + i ** 2) ) )
                    except Exception as e:
                        log( "%s catched, type = %s. Raising" % (e, type( e )) )
                        raise e

            return method

        from methods import methods
        for higher in methods:
            self.__setattr__( higher, IntermediateApiMethodsClass() )
            for lower in methods[higher]:
                self.__getattribute__( higher ).__setattr__( lower, callable_method( self, '.'.join( ( higher, lower ) ) ) )

    # Origins: https://github.com/dimka665/vk/tree/master/vk, 26.02.2016
    def get_new_access_token( self, timeout = 2, number_of_tries = 10 ):
        TIMEOUT = timeout
        LOGIN_URL = 'https://m.vk.com'
        AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
        CAPTCHA_URI = 'https://m.vk.com/captcha.php'

        if None in ( self.LOGIN, self.PASSWORD ):
            self.ACCESS_TOKEN = ""
            self.token_birth = datetime.now()
            self.token_expires_in = 0
            return ""

        session = requests.Session()
        session.headers['Accept'] = 'application/json'
        session.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        def get_form_action( html ):
            form_action = re.findall( '<form(?= ).* action="(.+)"', html )
            if form_action:
                return form_action[0]

        def timeout_handler( func, timeout = TIMEOUT ):
            def _f( timeout = timeout ):
                for i in range( number_of_tries ):
                    if i > 0: log( "iteration %i" % i )
                    try:
                        return func( timeout )
                    except requests.exceptions.ReadTimeout as e:
                        timeout = timeout * 2
                        log( '%s catched. Increasing timeout 2 times, %ss now' % (e, timeout ) )
                        time.sleep( 0.2 )
                    except requests.exceptions.ConnectionError as e:
                        timeout = timeout * 2
                        log( '%s catched. Increasing timeout 2 times, %ss now, and sleeping for %ss' % (e, timeout, 1 + i * timeout) )
                        time.sleep( 0.2 )
            return _f

        @timeout_handler
        def login( timeout ):
            response = session.get( LOGIN_URL, timeout = timeout )
            login_form_action = get_form_action( response.text )
            if not login_form_action:
                raise Exception('VK changed login flow')

            login_form_data = { 
                "email": self.LOGIN,
                "pass": self.PASSWORD
            }
            
            response = session.post( login_form_action, data = login_form_data, timeout = timeout )
            response_url_query = get_url_query( response.url )

            if 'remixsid' in session.cookies or 'remixsid6' in session.cookies:
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

        @timeout_handler
        def oauth2_authorization( timeout ):
            auth_data = {
                'client_id': self.APP_ID,
                'display': 'mobile',
                'response_type': 'token',
                'scope': self.SCOPE,
                'v': self.V,
                'lang': self.LANG
            }
            response = session.post( AUTHORIZE_URL, auth_data, timeout = timeout )
            response_url_query = get_url_query( response.url )
            if 'access_token' in response_url_query:
                return response_url_query
            
            form_action = get_form_action( response.text )
            if form_action:
                response = session.get( form_action, timeout = timeout )
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
        
        # log( auth_response_url_query )
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
        try: return self.s.get( url, timeout = timeout ).json()
        except Exception as e: log( "Catched an error: %s" % e )

    def __parse_response( self, response ):
        try: 
            return response['response']
        except: 
            try: exception = VkApiException( response['error'] )
            except Exception as e: exception = e
        raise exception

if __name__ == "__main__":
    api = VkApi( login = None, password = None )
    print( api.users.get( user_id = 1 ) )

    # To call this, setup login and password first
    # print( json.dumps( api.messages.get(), indent = 4, ensure_ascii = False ) ) 

