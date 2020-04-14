from django.shortcuts import render
import requests
import sys
from subprocess import run, PIPE


# Button to press to run the test prompt
def button(request):
    return render(request, "home.html")


""" Sample website
def output(request):
    data = requests.get("https://google.com/")
    print(data.text)
    data = data.text
    return render(request, 'home.html', {'data': data})
"""


# Code to run the program. Fix what is in '/Users/...' with path of program to run on personal device
def djangoTest(request):
    inp = request.POST.get("param")
    out = run([sys.executable, '/Users/eddiexu/Desktop/djangoTest/test.py', inp], shell=False, stdout=PIPE)
    print(out)

    return render(request, 'home.html', {'data1': out.stdout})
