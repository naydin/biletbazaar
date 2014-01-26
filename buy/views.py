# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context,loader
from data.models import *
from django.shortcuts import render,redirect

import datetime
import re

def biletal1(request):
    return render(request,'buy/biletal1.html')
    
def biletal2(request):
    return render(request,'buy/biletal2.html')
    
def biletal3(request):
    return render(request,'buy/biletal3.html')
    
def biletal4(request):
    return render(request,'buy/biletal4.html')