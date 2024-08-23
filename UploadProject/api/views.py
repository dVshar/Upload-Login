import hashlib
from api import utils

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from rest_framework import viewsets

from .models import *


# Create your views here.
class AuthAPI(viewsets.ModelViewSet):
    def get_user_is_login(self,request):
        try:
            token = request.GET.get('token',None)
            #decode token
            decoded_token = utils.decode_token(token)

            email = decoded_token['email']

            check_user = UsersTable.objects.get(email=email)
            if check_user:
                return JsonResponse({"status":True})
            else:
                return JsonResponse({"status":False})
        except:
            return JsonResponse({'status':False})
    
    def login_user(self,request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            print(hashed_password)

            check_user = UsersTable.objects.filter(email=email,password=hashed_password).first()
            if check_user:
                return JsonResponse({"token":"None","message":"Bad credentials","status":False})

            payload = {
                'email': email
            }

            token = utils.encode_token(payload)
            
            return JsonResponse({"token": token, "message": "Login successful","status":True})
        except:
            return JsonResponse({"token":"None","message":"Bad creds","status":False})


class User_Management(viewsets.ModelViewSet):
    def get_all_users(self,request):
        # try:
            token = request.GET.get('token',None)
            #decode token
            data = utils.decode_token(token)
            user = UsersTable.objects.get(email=data['email'])
            if(user.is_admin):
                all_users=[]
                users = UsersTable.objects.all()
                for i in users:
                    all_users.append({
                        "email":i.email,
                        "name":i.name
                    })
            else:
                all_users = []
            return JsonResponse({"Users":all_users})
        
        # except:
        #     return JsonResponse({"Users":[],"message":"API Failed"})
    
    def add_new_user(self,request):
        try:
            token = request.GET.get('token',None)
            #decode token
            data = utils.decode_token(token)

            user_check = UsersTable.objects.filter(email=data['email']).first()
            if user_check.is_admin:
                data = request.data
                email = data.get('email','None')
                password = data.get('password','None')
                name = data.get('name','None')

                check_user = UsersTable.objects.filter(email=email).first()
                if not check_user:
                    user = UsersTable.objects.create(
                        name = name,
                        email = email,
                        password = password
                    ).save()
                else:
                    return JsonResponse({"message":"User exists with same email"})
            else:
                return JsonResponse({"message":"Not authorize to add"})
            return JsonResponse({"message":"User Added Successfully"})
        except:
            return JsonResponse({"message":"API Failed"})
    
    def delete_user(self,request):
        try:
            data = request.data
            email = data.get('email')
            token = request.GET.get('token',None)
            decoded = utils.decode_token(token)
            user_check = UsersTable.objects.filter(email=decoded['email']).first()
            if user_check.is_admin:
                check_user = UsersTable.objects.filter(email=email).first()
            if not check_user:
                return JsonResponse({"message":"User not exists"})
            else:
                check_user.delete()
            return JsonResponse({"message":f"User deleted"})
        except:
            return JsonResponse({"message":"API Failed"})
