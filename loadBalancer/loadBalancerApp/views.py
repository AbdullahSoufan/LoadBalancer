import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Bit
from . serializer import bookSerializer, bookSerializer2


class bookList(APIView) :
    def get(self,request,topic_name):
        bitreplica = Bit.objects.get(id=1)
        bit=bitreplica.ReplicaBit
        if bit ==0:
            books_with_specific_topic = requests.get('http://127.0.0.1:8001/search/' + str(topic_name) + '/', params=request.GET,
                               timeout=5)
            data = books_with_specific_topic.text

            jsondata = json.loads(data)
            bitreplica.ReplicaBit=1
            bitreplica.save()
            return Response(jsondata)
        else:
            books_with_specific_topic = requests.get('http://127.0.0.1:8003/search/' + str(topic_name) + '/',
                                                     params=request.GET,
                                                     timeout=5)
            data = books_with_specific_topic.text

            jsondata = json.loads(data)
            bitreplica.ReplicaBit = 0
            bitreplica.save()
            return Response(jsondata)

class bookList2(APIView):
    def get(self,request,id):
        book = requests.get('http://127.0.0.1:8005/info/' + str(id) + '/',
                                                 params=request.GET,
                                                 timeout=5)
        if json.loads(book.text):
            data = book.text

            jsondata = json.loads(data)
            return Response(jsondata)
        else:
            bitreplica = Bit.objects.get(id=1)
            bit = bitreplica.ReplicaBit
            if bit == 0:
                books_with_specific_topic = requests.get('http://127.0.0.1:8001/info/' + str(id) + '/',
                                                         params=request.GET,
                                                         timeout=5)
                data = books_with_specific_topic.text

                jsondata = json.loads(data)
                bitreplica.ReplicaBit = 1
                bitreplica.save()
                requests.post('http://127.0.0.1:8005/update/' + str(id) + '/',
                                                         data=jsondata[0],
                                                         timeout=5)
                return Response(jsondata)
            else:
                books_with_specific_topic = requests.get('http://127.0.0.1:8003/info/' + str(id) + '/',
                                                         params=request.GET,
                                                         timeout=5)
                data = books_with_specific_topic.text

                jsondata = json.loads(data)
                bitreplica.ReplicaBit = 0
                bitreplica.save()
                requests.post('http://127.0.0.1:8005/update/' + str(id) + '/',
                              data=jsondata[0],
                              timeout=5)
                return Response(jsondata)
    def put(self,request,id):
        bitreplica = Bit.objects.get(id=1)
        bit = bitreplica.ReplicaBit
        if bit == 0:
           response=requests.put('http://127.0.0.1:8000/purchase/' + str(id) + '/',
                                                     params=request.GET,
                                                     timeout=5)
           bitreplica.ReplicaBit = 1
           bitreplica.save()
           return Response(response)

        else:
            response=requests.put('http://127.0.0.1:8004/purchase/' + str(id) + '/',
                                                     params=request.GET,
                                                     timeout=5)
            bitreplica.ReplicaBit = 0
            bitreplica.save()

            return Response(response)

