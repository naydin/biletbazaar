# -*- coding: utf-8 -*-
import re

class validation_util(object):
    @staticmethod
    def is_all_char_with_whitespace(str):
        return re.match(u"^[A-Za-z\sÇçŞşÜüÖöIıİiĞğ]+$", str,re.UNICODE)

    @staticmethod
    def is_all_char(str):
        return re.match(u"^[A-Za-zÇçŞşÜüÖöIıİiĞğ]+$", str,re.UNICODE)

    @staticmethod
    def is_address(str):
        return re.match(u"^[0-9A-Za-z:,-./\sÇçŞşÜüÖöIıİiĞğ]+$",str,re.UNICODE)

    @staticmethod
    def is_all_digit(str):
        return re.match(u"^[0-9]+$", str, re.UNICODE)
        
    @staticmethod
    def is_password(str):
        #TODO:password validation should be added
        return True

    @staticmethod
    def is_gsm(str):
        #TODO:gsm validation should be added
        return True

