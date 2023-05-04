from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,serializers
from rest_framework.response import Response 
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from django.db import connection
from .public_fuctions import get_profile_image_for_comment,dictfetchall
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserRenderer
import json
from .UUIDEncoder import UUIDEncoder,popstate

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserAuthenticationViews(APIView):
    renderer_classes=[UserRenderer]
    def get(self,request):
        return Response({"msg":"data is fetched"})
    def post(self,request):
        
        serializeddata=UserAuthenticationSerializer(data=request.data)
        if serializeddata.is_valid(raise_exception=True):
            user=serializeddata.save()
            token=get_tokens_for_user(user)
            return Response({"token":token,"msg":"registration completed sucessfully"},status=status.HTTP_201_CREATED)
        
        return Response({"msg":"data is invalid"},status=status.HTTP_400_BAD_REQUEST)

class LoginAuthenticationViews(APIView):
    renderer_classes=[UserRenderer]

    def post(self,request):
        serializeddata=LoginAuthenticateSerializer(data=request.data)
        if serializeddata.is_valid(raise_exception=True):
            email=serializeddata.data.get('email')
            password=serializeddata.data.get('password')
            try:
                user=User.objects.get(email=email)
            except:
                user=None
            

            if user is not None:
                if user.check_password(password):
                    token=get_tokens_for_user(user)
                    
                    return Response({"token":token,"username":user.username,"msg":"user registration sucessfull"},status=status.HTTP_200_OK)
                else:
                    return Response({"errors":{"password":"Password is incorrect"}},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"errors":{"email":"User with this email doesn't exists"}},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializeddata.errors,status=status.HTTP_400_BAD_REQUEST)
    








class PostView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
 
    def get(self,request,pk):
      
        with connection.cursor() as cursor:
            cursor.execute("SELECT username,title,contentvalue,link,post_type,account_content.id from account_user LEFT JOIN account_content on account_user.id=account_content.posted_by_id  where account_content.id=%s",[pk])
            data=dictfetchall(cursor)[0]
            cursor.execute("SELECT username,account_comments.id,post_id,comment from account_user LEFT JOIN account_comments on account_user.id=account_comments.commented_by WHERE  account_comments.post_id=%s",[pk])
            data.update({"comments":dictfetchall(cursor)})
          
            return Response(data,status=status.HTTP_200_OK)
        return Response({"errors":{"post":"post not found"}})
        


   

class GetPostsView(APIView):
    def get(self,request,pk=None):
   
        with connection.cursor() as cursor:
            cursor.execute("SELECT username,title,contentvalue,link,post_type,account_content.id from account_user RIGHT JOIN account_content on account_user.id=account_content.posted_by_id ORDER BY id ASC ")
            data=dictfetchall(cursor)
        return Response(data)
        
        
        


    def post(self,request,pk=None):
           
        serialized_data=PostsSerializer(data=request.data)
        data=request.data
        if serialized_data.is_valid(raise_exception=True):
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO account_content(posted_by_id,title,link,contentvalue,post_type) VALUES (%s,%s,%s,%s,%s)",[request.user.id,data["title"],data["link"],data["contentvalue"],data["post_type"]])
                return Response("Successfully saved")
        else:
            return Response("Some error occured")
    def put(self,request,pk=None):
       

        serialized_data=PostsSerializer(data=request.data)
        data=request.data
        if serialized_data.is_valid(raise_exception=True):
            with connection.cursor() as cursor:
                cursor.execute("UPDATE account_content SET title=%s, contentvalue=%s, post_type=%s,link=%s WHERE id=%s",[data["title"],data["contentvalue"],data["post_type"],data["link"],pk])
                return Response("Successfully saved")
        else:
            return Response("Some error occured")
    
    def delete(self,request,pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM account_content WHERE id=%s",[pk])
            cursor.execute("SELECT * FROM account_content WHERE posted_by_id=%s",[request.user.id])

            requiredvalues=dictfetchall(cursor)
        return Response(requiredvalues) 
        
            
        



class AddCommentView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,pk):
        # objectall=Content.objects.get(postid=pk)
        # username=objectall.posted_by.username
        # objectall.comments.append([request.user.username,request.data["comment"]])
        # objectall.save()
        # serializeddata=UUIDEncoder(objectall.__dict__)
        # serializeddata["comments"]=get_profile_image_for_comment(serializeddata["comments"])
        # serializeddata.update({"username":username})
        data=request.data
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO account_comments(post_id,comment,commented_by) VALUES (%s,%s,%s)",[pk,data["comment"],request.user.id])
            # cursor.execute("SELECT username,title,contentvalue,link,post_type,account_content.id from account_user LEFT JOIN account_content on account_user.id=account_content.posted_by_id WHERE account_content.id=%s",[pk])
            # data=dictfetchall(cursor)[0]
            # cursor.execute("SELECT * FROM account_comments  where post_id=%s",[pk])
            # data.update({"comments":dictfetchall(cursor)})
            cursor.execute("SELECT username,title,contentvalue,link,post_type,account_content.id from account_user LEFT JOIN account_content on account_user.id=account_content.posted_by_id  where account_content.id=%s",[pk])
            data=dictfetchall(cursor)[0]
            cursor.execute("SELECT username,account_comments.id,post_id,comment from account_user LEFT JOIN account_comments on account_user.id=account_comments.commented_by WHERE  account_comments.post_id=%s",[pk])
            data.update({"comments":dictfetchall(cursor)})
                    
            return Response(data,status=status.HTTP_200_OK)

        return Response("Some Error occured")

class GetMyPostsViews(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        # requiredvalues=Content.objects.filter(posted_by=request.user).values("forum","postid","title","contentvalue","comments","likes")
        # requiredvalues=[{"forum":Forums.objects.get(forumid=i["forum"]).forum_name,"postid":str(i["postid"]),"title":i["title"],"content":i["contentvalue"],"comments_count"
        # :len(i["comments"]),"likes":i["likes"]
        # } for i in requiredvalues]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM account_content WHERE posted_by_id=%s ",[request.user.id])
            requiredvalues=dictfetchall(cursor)
        return Response(requiredvalues)

class GetpostData(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM account_content  where id=%s",[pk])
            data=dictfetchall(cursor)[0]
            return Response(data)
        return Response("Some Error occured")

class GetALLDetails(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT email,username FROM account_user WHERE id=%s",[request.user.id])

            data=dictfetchall(cursor)[0]
            cursor.execute("SELECT COUNT(contentvalue) FROM account_content WHERE posted_by_id=%s",[request.user.id])
            data.update({"content_count":dictfetchall(cursor)[0]["COUNT(contentvalue)"]})
            cursor.execute("SELECT COUNT(comment) FROM account_comments WHERE commented_by=%s",[request.user.id])

            data.update({"comment_count":dictfetchall(cursor)[0]["COUNT(comment)"]})
            return Response(data)
        return Response("Some Error occured")



        



    