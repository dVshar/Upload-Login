import hashlib
from api import utils

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from rest_framework import viewsets

from .models import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
import base64
import ast
from email.message import EmailMessage
from email.mime.text import MIMEText
from datetime import datetime


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
            if not check_user:
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
        # try:
            token = request.GET.get('token',None)
            #decode token
            data = utils.decode_token(token)

            user_check = UsersTable.objects.filter(email=data['email']).first()
            if user_check.is_admin:
                user_data = request.data
                email = user_data.get('email','None')
                password = user_data.get('password','None')
                name = user_data.get('name','None')

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
        # except:
        #     return JsonResponse({"message":"API Failed"})
    
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


class AuthorityLetters(viewsets.ModelViewSet):
    def get_all_letters_list(self,request):
        return JsonResponse({"letters":[],"status":True})
    
    def add_new_letters_in_list(self,request):
        return JsonResponse({"message":"Added to list","status":True})
    

def send_email(subject, body, sender,password, recipients):
    try:
        # Create a MIME message
        msg = MIMEText(body,'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        # Attach the HTML body
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)
    

class SendMail(viewsets.ModelViewSet):
    def send_email_funtion(self,request):
        data = request.data
        tag = data.get('tag')
        if tag=="contact":
            mail_message = data.get("message")

            Name = mail_message.get("Name")
            Contact = mail_message.get("Contact")
            email = mail_message.get("email")
            country = mail_message.get("country")
            message = mail_message.get("message")
            to_email = mail_message.get("to_email")

            From = "eazotelservice@gmail.com"
            password = "xshqkvxwkdjumehh"
            to = to_email.split(',')
            Subject = "Query Raised on ThkTrade Website"
            body = '''
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="padding:20px 0px">
                        <p> Dear Sir, </p>
                        <p> We have recieved the query from you on website. Here are the details for the query </p>
                        <p>Name: {} </p>
                        <p>Contact: {}</p>
                        <p>Email-Id: {} </p>
                        <p>Country: {}</p>
                        <p>Message: {}</p>    
                    </div>
                </body>
                </html>
            '''.format(Name,Contact,email,country,message)
            send_email(subject=Subject, body=body, sender=From, recipients=to,password=password)

        return JsonResponse({"message":"Sent"})