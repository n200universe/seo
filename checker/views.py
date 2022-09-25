from turtle import position
from typing import List
from django.shortcuts import render
import time
import datetime
# import pandas as pd
from ecommercetools import seo
from yaml import serialize

from checker.models import Projects
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from rest_framework.views import APIView
from rest_framework.response import Response


from .models import KeywordsChecker, Projects
from .serializers import ProjectsSerializer, KeywordsCheckerSerializer

class ListCreateProjectsView(ListCreateAPIView):
    model = Projects
    serializer_class = ProjectsSerializer
    parser_classes = [JSONParser]

    def get_queryset(self):
        return Projects.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message:': 'Đã tạo project mới thành công',
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Tạo dự án mới không thành công.'
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteProjectsView(RetrieveUpdateDestroyAPIView):


    def get_queryset(self):
        return Projects.objects.all()
    model = Projects
    serializer_class = ProjectsSerializer

    def put(self, request, *args, **kwargs):
        project = get_object_or_404(Projects, id=kwargs.get('pk'))
        serializer = ProjectsSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                 'message:': 'Đã cập nhật dự án mới thành công',
            }, status = status.HTTP_200_OK)
        return JsonResponse({
                'message:': 'Cập nhật dự án mới không thành công',

        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Projects,id=kwargs.get('pk'))
        project.delete()
        return JsonResponse({
                            'message:': 'Xoá dự án mới thành công',

        }, status=status.HTTP_200_OK)


class ListCreateKeywordsCheckerView(ListCreateAPIView):
    model = KeywordsChecker
    serializer_class = KeywordsCheckerSerializer
    # queryset = KeywordsChecker.objects.all()
    filterset_fields = ['project', 'id']
    parser_classes = [JSONParser]

    def get_queryset(self, *args, **kwargs):
        # project = get_object_or_404(Projects, id=kwargs.get["pk"])
        return KeywordsChecker.objects.all()

    def perform_create(self, serializer):

        serializer = KeywordsCheckerSerializer(data=self.request.data)
               
        project = Projects.objects.get(id=self.request.data["project"])

        # GETTING KEYWORD LISTS OF THE PROJECT:
        project_keywords = KeywordsChecker.objects.filter(project__id = project.id)
        project_keywords_list = project_keywords.values_list('keyword')

        print(project_keywords_list) 
        # CHECK IF KEYWORD EXIST IN KEYWORD LISTS:

        keywords = self.request.data['keyword']
        keyword_lists = []

        if "," in keywords:
            print(", in keywords")
            print(keywords.split(','))
            keyword_lists.append(keywords.split(","))

        else:
            keyword_lists.append(keywords)

            print(keywords)

        print(keyword_lists)
        # # GET KEYWORD LIST INPUT
        # if "," in keywords:

        #     keyword_lists = keyword_lists.append(keywords.split(","))
        # else:
        #     keyword_lists = keyword_lists.append(keywords)
        i = 0
        while i <= len(keyword_lists):
             
            print("i now : "+str(i))
            for keyword in keyword_lists:
                print(keyword)
                if any(keyword in i for i in project_keywords_list):
                    # IF EXISTED: UPDATE THE POSITION IF POSITION IS CHANGED

                    print("Keyword is already in the list")
                    return JsonResponse({
                        'message:': 'Từ khoá đã tồn tại trong danh sách.',
                    }, status=status.HTTP_201_CREATED)
                else:
                    print("Keyword not existed, creating new one to list")
                    # get the domain from request > project > domain
                    domain = project.domain

                    # get the 5 pages result by keyword
                    df = seo.get_serps(keyword, pages=5)

                    # get the first position of keyword with the domain provided
                    data = df[df['link'].str.startswith(domain)].head(1).to_dict('records')

                    if len(data) > 0:
                        print("Vị trí: "+str(data[0]["position"]))
                        position_checked = data[0]["position"]

                        if serializer.is_valid():
                            if position_checked != "":

                                serializer.save(keyword=keyword, position=position_checked, url=data[0]["link"],
                                title =data[0]['title'], meta_description = data[0]['text'],
                                first=position_checked,best=position_checked, change="0"
                                )
                                return JsonResponse({
                                    'message': 'Đã tạo từ khoá mới thành công',
                                }, status=status.HTTP_201_CREATED)
                            else:
                                serializer.save(position="getting", url="",
                                title ="", meta_description = "",
                                first="",best="", change=""
                                )
                                return JsonResponse({
                                    'message': 'Đã tạo từ khoá mới thành công',
                                }, status=status.HTTP_201_CREATED)

                        else:
                            
                            return JsonResponse({
                                'message': 'Tạo từ khoá mới không thành công.'
                            }, status=status.HTTP_400_BAD_REQUEST)


                    else:
                        if serializer.is_valid():
                            serializer.save(keyword=keyword
                            )
                            return JsonResponse({
                                'message': 'Đã tạo từ khoá mới thành công',
                            }, status=status.HTTP_201_CREATED)
                    i+=1

                            
class UpdateDeleteKeywordsCheckerView(RetrieveUpdateDestroyAPIView):


    model = KeywordsChecker
    serializer_class = KeywordsCheckerSerializer
    # lookup_field="id"
    parser_classes = [JSONParser]


    def get_queryset(self):
        return KeywordsChecker.objects.all()

    def put(self, request, *args, **kwargs):
        keywords = get_object_or_404(KeywordsChecker, id=kwargs.get('pk'))
        serializer = KeywordsCheckerSerializer(keywords, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                 'message:': 'Đã cập nhật từ khoá mới thành công',
            }, status = status.HTTP_200_OK)
        return JsonResponse({
                'message:': 'Cập nhật từ khoá mới không thành công',

        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(KeywordsChecker,id=kwargs.get('pk'))
        project.delete()
        return JsonResponse({
                            'message:': 'Xoá từ khoá mới thành công',

        }, status=status.HTTP_200_OK)
    def patch(self, request,pk):
        testmodel_object = self.get_object(pk)
        serializer = KeywordsCheckerSerializer(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            print("Save updated")
            return JsonResponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")


# UPDATE KEYWORD POSITION
class DetailKeywordView(APIView):
    parser_classes = [JSONParser]
    model = KeywordsChecker
    serializer_class = KeywordsCheckerSerializer
    filterset_fields = ['project', 'id']

    def get_queryset(self, pk, *args, **kwargs):
        # project = get_object_or_404(Projects, id=kwargs.get["pk"])
        return KeywordsChecker.objects.get(pk=pk)
    def get_object(self, pk):
        return KeywordsChecker.objects.get(pk=pk)

    def delete(self, request, pk, format=None):
        keyword_object = self.get_object(pk)
        keyword_object.delete()
        # serializer = KeywordsCheckerSerializer(keyword_object, data=request.data) # set partial=True to update

        return Response(status=status.HTTP_204_NO_CONTENT)

    

    def patch(self, request, pk):
        # serializer = KeywordsCheckerSerializer(data=self.get_object(pk=pk), many=True)
        keyword_object = self.get_object(pk)
        serializer = KeywordsCheckerSerializer(keyword_object, data=request.data, partial=True) # set partial=True to update

        # GET ID=PK > KEYWORD > CHECK POSITION
        keyword_object = self.get_object(pk)

        # GET THE CURRENT POSITION 

        if keyword_object.position != None:
            current_position = int(keyword_object.position)

        # GET THE BEST POSITION
        if keyword_object.best != None:
            best_position = int(keyword_object.best)

        # GET THE FIRST POSITION
        if keyword_object.first != None:
            first_position = int(keyword_object.first)

        # GET THE NEW POSITION: required (domain, keyword)
        keyword = keyword_object.keyword
        project_id = keyword_object.project.id
        print("Keyword: "+ str(keyword))

        # get project > domain
        project_object= Projects.objects.get(id=project_id)
        domain = project_object.domain
        print("Domain "+str(domain))

        # get the 5 pages result by keyword
        df = seo.get_serps(keyword, pages=5)

        # get the first position of keyword with the domain provided
        data = df[df['link'].str.startswith(domain)].head(1).to_dict('records')
        
        change = 0
        # from time import sleep
        # sleep(2)
        if len(data) > 0:
            print("Vị trí cập nhật: "+str(data[0]["position"]))
            new_position = int(data[0]["position"])

            # new_position = position_checked

                # thay đổi ? mới nhất ? tốt nhất? đầu tiên
                # đầu tiên ko thay đổi
                # mới nhất vs thay đổi > trừ ra = mới nhất - đầu tiền?
                # mới nhất vs tốt nhất: mới < tốt => tốt = mới; mới >= tốt: ko thay đổi; 

            # 1.update current position, if new posiion < current position & new < best => best_position = new
        
            
            change = first_position - new_position

            if new_position<current_position:
                print("new BETTER position found")
                best_position = new_position


            elif new_position > current_position:
                print("new WORSER position found") 


            else:
                print("Nothing changes")
                

            if serializer.is_valid():
                print("Validated")

                serializer.save(position=new_position, url=data[0]["link"],
                                    title =data[0]['title'], meta_description = data[0]['text'],
                                    best=best_position, change=change,
                                    )            
                print("Save updated")
                return JsonResponse(status=204, data=serializer.data, safe=False)            

            else:
                return JsonResponse(status=402, data="wrong parameters", safe=False)

        else:
            if serializer.is_valid():
                print("Validated")

                serializer.save(
                                    )            
                print("Saved updated")
                return JsonResponse(status=204, data=serializer.data, safe=False)            

            else:
                return JsonResponse(status=402, data="wrong parameters", safe=False)

class UpdateKeywordByProject(APIView):
    # MAIN CONCEPT: TO UPDATE LIST OF KEYWORD IN A PROJECT > GET PROJECT ID > GET LIST OF KEYWORD > PATCH EACH OF KEYWORD
    parser_classes = [JSONParser]
    model = KeywordsChecker
    serializer_class = KeywordsCheckerSerializer
    filterset_fields = ['project', 'id']

    # def get_queryset(self, pk, *args, **kwargs):
    #     # project = get_object_or_404(Projects, id=kwargs.get["pk"])
        # return KeywordsChecker.objects.get(pk=pk)
    def get_object(self, pk):
        return KeywordsChecker.objects.get(pk=pk)

    def get_queryset(self):
        project = self.kwargs["pk"]
        # return KeywordsChecker.objects.filter(project__id=project)
        return KeywordsChecker.objects.all()

    def patch(self, request, pk):

        # UPDATE BY PROJECT ID
        # 1. get the project id: using get_queryset above or
        project_id = self.kwargs["pk"]
        print(pk)
        print(project_id)
        
        # 2. get all the keywords of that project id
        keywords_project = KeywordsChecker.objects.filter(project__id=project_id)
        print("Keywords:"+str(keywords_project))

        # 3. run update for all keywords: using loop

        for keyword in keywords_project:

                print("Keyword list: " + str(keyword))
                serializer = KeywordsCheckerSerializer(keyword, data=request.data, partial=True) # set partial=True to update
                print(keyword.position)


                # GET ID=PK > KEYWORD > CHECK POSITION
                keyword_object = keyword

                if keyword_object.position != None:
                    current_position = int(keyword_object.position)

                # GET THE BEST POSITION
                if keyword_object.best != None:
                    best_position = int(keyword_object.best)

                # GET THE FIRST POSITION
                if keyword_object.first != None:
                    first_position = int(keyword_object.first)
                # GET THE NEW POSITION: required (domain, keyword)
                keyword = keyword_object.keyword
                project_id = keyword_object.project.id

                # get project > domain
                project_object= Projects.objects.get(id=project_id)
                domain = project_object.domain
                print("Domain "+str(domain))

                # get the 5 pages result by keyword
                df = seo.get_serps(keyword, pages=5)

                # get the first position of keyword with the domain provided
                data = df[df['link'].str.startswith(domain)].head(1).to_dict('records')
                
                change = 0
                # from time import sleep
                # sleep(2)
                if len(data) > 0:
                    print("Vị trí cập nhật: "+str(data[0]["position"]))
                    new_position = int(data[0]["position"])
                    
                    change = first_position - new_position

                    if new_position<current_position:
                        print("new BETTER position found")
                        best_position = new_position


                    elif new_position > current_position:
                        print("new WORSER position found") 


                    else:
                        print("Nothing changes")
                    
                
                    if serializer.is_valid():
                        print("Validated")

                        serializer.save(position=new_position, url=data[0]["link"],
                                            title =data[0]['title'], meta_description = data[0]['text'],
                                            best=best_position, change=change,
                                            )            
                        print("Save updated")
                        return JsonResponse(status=204, data=serializer.data, safe=False)            
                    else:
                        return JsonResponse(status=402, data="wrong parameters", safe=False)
                    

                else:
                    if serializer.is_valid():
                        print("Validated")

                        serializer.save()            
                        print("Saved updated")
                        return JsonResponse(status=204, data=serializer.data, safe=False)            

                    else:
                        return JsonResponse(status=402, data="wrong parameters", safe=False)
        
# class BulkUpdateKeywords(ListSer)



#get keyword list from porject ID
class KeywordsList(ListAPIView):
    serializer_class = KeywordsCheckerSerializer

    def get_queryset(self):
        project = self.kwargs["projectId"]
        return KeywordsChecker.objects.filter(project__id=project)

   
# class UpdateBulkKeywords()