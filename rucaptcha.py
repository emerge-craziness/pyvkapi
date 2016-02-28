# -*- coding: utf-8 -*-

# Origin: https://github.com/vit1251/ru_captcha/blob/master/ru_captcha.py, 14.12.2015

import os
import time
import logging
import threading
import requests

class RUCaptchaThreading(threading.Thread):
    def __init__(self, apikey, interval=5):
        threading.Thread.__init__(self)
        self.__interval = interval
        self.__queue = []
        self.__apikey = apikey

    def register(self, item):
        assert isinstance(item, RUCaptchaValue)
        self.__queue.append(item)

    def stop(self):
        self.__running = False

    def __check_values(self, log = False ):
        # if log:
            # print("Monitoring values: {count!r}".format(count=len(self.__queue)))
        queue = []
        for item in self.__queue:
            captcha_id = item.get_captcha_id()
            url = "http://rucaptcha.com/res.php?key={apikey}&action=get&id={captcha_id}".format( apikey=self.__apikey, captcha_id=captcha_id )
            r = requests.get( url )
            if r.status_code == 200:
                if "CAPCHA_NOT_READY" in r.content.decode():
                    # print("Capcha not ready.")
                    queue.append(item)
                elif "|" in r.content.decode():
                    code, value = r.content.decode().split("|", 1)
                    if code == "OK":
                        item.set_value(value)
                        item.ready()
                    else:
                        print("Error code: {code!r} => {value!r}".format(code=code, value=value))
                else:
                    print("Unknown response: {response!r}".format(response=r.content.decode()))

        self.__queue = queue

    def run(self):
        self.__running = True
        while self.__running is True:
            self.__check_values()
            #
            time.sleep(self.__interval)


class RUCaptchaValue(object):
    def __init__(self, captcha_id, timeout=20):
        self.__ready = False
        self.__value = None
        self.__captcha_id = captcha_id
        self.__start = time.time()
        self.__timeout = timeout

    def set_value(self, value):
        self.__value = value

    def ready(self):
        self.__ready = True

    def is_expire(self):
        result = False
        interval = time.time() - self.__start
        if interval > self.__timeout:
            result = True
        return result

    def get_captcha_id(self):
        return self.__captcha_id

    def is_ready(self):
        return self.__ready

    def get_value(self):
        return self.__value

    def __repr__(self):
        result = "<RUCaptchaValue is_ready={ready!r} value={value!r} expire={expire!r}>".format(ready=self.__ready, value=self.__value, expire=self.is_expire())
        return result


class RUCaptcha( object ):
    def __init__( self, apikey, rtimeout=5, mtimeout=15, checking_interval = 1 ):
        self.__monitoring = RUCaptchaThreading( apikey=apikey, interval = checking_interval )
        self.__monitoring.start()
        self.__apikey = apikey
        self.__rtimeout = rtimeout
        self.__mtimeout = mtimeout
        self.__checking_interval = checking_interval

    def dispose( self ):
        if self.__monitoring is not None:
            self.__monitoring.stop()
            self.__monitoring = None

    def __check_response( self, content ):
        content = content.decode()
        if content is not None:
            if "|" in content:
                code, captcha_id = content.split('|', 1)
                if code == "OK":
                    print("captcha_id: {captcha_id!r}".format( captcha_id = captcha_id ) )
                    ru_captcha_value = RUCaptchaValue( captcha_id = captcha_id )
                    self.__monitoring.register( ru_captcha_value )
                    return ru_captcha_value
        return None

    def parse( self, path, use_multithreading = False, **kwargs ):
        """
        Дополнительные параметры капчи (kwargs):
            is_phrase       0 OR 1 - капча из двух или более слов
            is_regsense     0 OR 1 - регистр ответа важен
            is_numeric      0 OR 1 OR 2 OR 3 - 0 = параметр не задействован (значение по умолчанию) 1 = капча состоит только из цифр 2 = Капча состоит только из букв 3 = Капча состоит либо только из цифр, либо только из букв.
            min_len         0 если не ограничено, иначе обозначает минимальную длинну ответа
            max_len         0 если не ограничено, иначе обозначает минимальную длинну ответа
            language        0 OR 1 OR 2  0 = параметр не задействован (значение по умолчанию) 1 = капча на кирилице 2 = капча на латинице
            mime            mime тип изображения, по умолчанию - image/jpeg
        """
        if os.path.isfile( path ): 
            filestream = open( path, 'rb' )
        else: 
            filestream = requests.get( path, stream = True ).raw    
        files = [
            ( 'file', ( 'captcha', filestream, kwargs.pop( 'mime', 'image/jpeg' ) ) )
        ]
        data = {
            'method'    : 'post',
            'key'       : self.__apikey, 
            'phrase'    : kwargs.pop( 'is_phrase', 0 ),
            'regsense'  : kwargs.pop( 'is_regsense', 0 ),
            'numeric'   : kwargs.pop( 'is_numeric', 0 ),
            'min_len'   : kwargs.pop( 'min_len', 0 ),
            'max_len'   : kwargs.pop( 'max_len', 0 ),
            'language'  : kwargs.pop( 'language', 0 )
        }
        url = 'http://rucaptcha.com/in.php'
        r = requests.post( url, files = files, data = data )
        if r.status_code == 200: 
            value_instance = self.__check_response( r.content )
        else: 
            value_instance = None

        if use_multithreading:
            return value_instance
        else:
            seconds = kwargs.pop( 'loop_delay', self.__checking_interval )
            while not value_instance.is_ready():
                time.sleep( seconds )
            return value_instance.get_value()


# if __name__ == "__main__":
#     ru_captcha = RUCaptcha(apikey="***")
#     value = ru_captcha.parse(path="tests/test_000.jpg", is_regsense=1)
#     #
#     print("{value!r}".format(value=value))
#     #
#     while not value.is_ready():
#         time.sleep(0.1)
#     #
#     print("{value!r}".format(value=value))
#     #
#     print(value.get_value())
#     #
#     ru_captcha.dispose()
