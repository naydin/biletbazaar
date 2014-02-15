import base64

class encode_util(object):
    @staticmethod
    def base64(str):
        return base64.b64encode(str)
        
class decode_util(object):
    @staticmethod
    def base64(str):
        return base64.b64decode(str)
        