from django.contrib.auth.models import User
from django.shortcuts import render
import pyrebase
import tweepy
from pythainlp.tokenize import word_tokenize as wt
import re
from rest_framework import request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.views.generic import View


#config
config = {
    'apiKey': "AIzaSyDciJr07mAlYjUx9WJXlZq5aCThWkHQi9I",
    'authDomain': "sentimentanalysis-d39db.firebaseapp.com",
    'databaseURL': "https://sentimentanalysis-d39db.firebaseio.com",
    'projectId': "sentimentanalysis-d39db",
    'storageBucket': "sentimentanalysis-d39db.appspot.com",
    'messagingSenderId': "922627858083",
    'appId': "1:922627858083:web:5ec636e24570f9be682916"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


# Create your views here.
def index(request):
    context = {"home_page":"active"}
    data = db.child('Sentiment').get().val()

    return render(request,'sentimental/index.html',{'comlis': data},context)
def contact(request):
    context = {"contact_page": "active"}
    return render(request,'sentimental/contact.html',context)
def about(request):
    context = {"about_page": "active"}
    return render(request,'sentimental/about.html',context)

def visual(request):

    return  render(request, 'sentimental/index1.html')
def table_search(request):

    return render(request, 'sentimental/table_search.html')

def table_show(request):


    return render(request, "sentimental/visulization.html")


class ChartData(APIView):
    authentication_classes = []
    permisson_classes = []
    
    def get(self,request, format =None):
        time = request.GET.get('z')
        work = db.child('Sentiment').child(time).get().val()
        work2 = dict(work)
        if "cluster" in work2:
            del work2["cluster"]

        data = {
            "data": work2,
        }
        return Response(data)




class ChartDataPositive(APIView):
    authentication_classes = []
    permisson_classes = []

    def get(self,request, format =None):
        time = request.GET.get('z')
        work1 = db.child('Sentiment').child(time).child('cluster').child('Positive').get().val()

        data = {
            "data": work1,
        }
        return Response(data)


class ChartDataNegative(APIView):
    authentication_classes = []
    permisson_classes = []

    def get(self,request, format =None):
        time = request.GET.get('z')
        work1 = db.child('Sentiment').child(time).child('cluster').child('Negative').get().val()


        data = {
            "data": work1,
        }
        return Response(data)


        
class ChartDataNeutral(APIView):
    authentication_classes = []
    permisson_classes = []

    def get(self,request, format =None):
        time = request.GET.get('z')
        work1 = db.child('Sentiment').child(time).child('cluster').child('Neutral').get().val()


        data = {
            "data": work1,
        }
        return Response(data)


def searchdata(request):

    z = request.GET.get('z')
    data = search_name(z)


    data1 = {
        "data" : data,
        "name" : z
    }


    return render(request,"sentimental/search.html",data1)




def search_name(search_terms):
    consumerKey = "INKFuJbdhm4umODXmXOzh9sRh"
    consumerSecret = "KES9DBLkBCnoe7QtRA8EdJNM6CODK2hMry4i44NxptItWhoHln"
    accessToken = "254573033-4eKzjAdSrjzLAdEL5aHCz0W0q30I1UI1uWIMlWc9"
    accessTokenSecret = "g3RhcTjZJnRJbuF6n4O9gjyGUe6dtDs8iIQROCk4DwXp2"

    auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    searchTerm = search_terms
    noOfSearchTerms = 200
    tweets = tweepy.Cursor(api.search, q=searchTerm, lang="th").items(noOfSearchTerms)
    data = []
    for tweet in tweets:
        data.append(tweet.text)

    def merge_text(text_array):
        temp = ""
        for data in text_array:
            temp += data + ' '
        return temp

    # Cut word with re and word_tokenize
    def handle_wt(txt):
        regx = r'https://t.co/\w+|RT\s@\w*\d*:|\n|\s|#|_|\u200b|[=]+\s[ก-๙]+\s[=]+|\n'  # regrx for handle url to split it.
        txt_ = merge_text(re.split(regx, txt))
        txt__ = merge_text(re.findall(r'[a-zA-Zก-๙]+', txt_, re.MULTILINE))
        text_raw = wt(txt__, engine='newmm')
        datas = list(filter(lambda x: x, text_raw))
        return datas

    # Clean text
    def clean_text(text):
        text = handle_wt(text)  # cut text to array
        texts = ' '.join(word.strip() for word in text if len(word) > 2)  # delete stopwors from text
        return texts

    data_clean = [clean_text(txt) for txt in data]

    return data_clean

