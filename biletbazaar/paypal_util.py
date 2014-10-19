import urllib
import urllib2
import json
from local_settings import *

sandbox_api_adaptive_pay_url = 'https://svcs.sandbox.paypal.com/AdaptivePayments/Pay'
sandbox_api_dummy_url = 'https://api-3t.sandbox.paypal.com/nvp'
sandbox_payment_page_url = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey='

api_caller_user_id = LOCAL_PAYPAL_API_CALLER_USER_ID
api_caller_password = LOCAL_PAYAPL_API_CALLER_PASSWORD
api_caller_signature = LOCAL_PAYPAL_API_CALLER_SIGNATURE
application_id = LOCAL_PAYPAL_APPLICATION_ID

http_header = {
    'X-PAYPAL-SECURITY-USERID':api_caller_user_id,
    'X-PAYPAL-SECURITY-PASSWORD':api_caller_password,
    'X-PAYPAL-SECURITY-SIGNATURE':api_caller_signature,
    'X-PAYPAL-APPLICATION-ID' :application_id,
    'X-PAYPAL-REQUEST-DATA-FORMAT':'JSON',
    'X-PAYPAL-RESPONSE-DATA-FORMAT':'JSON'
}

class paypal_util(object):

    @staticmethod
    def payment_url(payKey):
        return sandbox_payment_page_url + payKey

    #returns pay key    
    @staticmethod
    def call_adaptive_payment(receiver_email, amount):
        params = {
            "returnUrl":"http://www.biletbosta.com",
            "requestEnvelope":{"errorLanguage":"en_US"},
            "currencyCode":"TRY",
            "receiverList":{"receiver":[{"email":receiver_email, "amount":amount}]},
            "cancelUrl":"http://www.biletbosta.com/anasayfa",
            "actionType":"PAY"
        }
    
        paymentRequest = urllib2.Request(sandbox_api_adaptive_pay_url, json.dumps(params), http_header)

        # debug code
        # handler=urllib2.HTTPSHandler(debuglevel=1)
        # opener = urllib2.build_opener(handler)
        # urllib2.install_opener(opener)
    
        try:
            resp = urllib2.urlopen(paymentRequest)
            jsonResponse = resp.read()
            jsonDictionary = json.loads(jsonResponse)
            payKey = jsonDictionary['payKey']
            
            return payKey
            
        except Exception as e:
            return None
    
    #returns raw data      
    @staticmethod  
    def call_dummy_request():
        params = {
            'DATA-FORMAT':'JSON',
            'USER':api_caller_user_id,
            'PWD':api_caller_password,
            'SIGNATURE':api_caller_signature,
            'METHOD':'SetExpressCheckout',
            'VERSION':'98',
            'PAYMENTREQUEST_0_AMT':'10',
            'PAYMENTREQUEST_0_CURRENCYCODE':'TRY',
            'PAYMENTREQUEST_0_PAYMENTACTION':'SALE',
            'cancelUrl':'http://www.biletbosta.com',
            'returnUrl':'http://www.biletbosta.com'

        }
    
        req = urllib2.Request(sandbox_api_dummy_url, urllib.urlencode(params))

        try:
            resp = urllib2.urlopen(req)
            return resp.read()
        except Exception as e:
            return None

