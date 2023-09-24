from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import threading

from . import models as common_model
from . import serilaizer as common_serializer
from . import tasks
from . import forms
from helpers import utils
from . import swagger_doc

class SignupApi(APIView):

    serializer_class= common_serializer.SignupSerializer
    model= common_model.User
    swagger_doc_item = swagger_doc.sign_up_post

    @swagger_auto_schema(
        tags=swagger_doc_item['tag'],
        operation_id=swagger_doc_item['url_name'],
        operation_description=swagger_doc_item['description'],
        request_body=openapi.Schema(
            
            required=swagger_doc_item['required_fields'],
            type=openapi.TYPE_OBJECT,
            properties = swagger_doc_item['fields'],
        ),
        responses=swagger_doc_item['responses'],
        
    )
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "status":200,
                "message":"Your account is created, Please login..",
            }
            )
        else:
            error_list = utils.serilalizer_error_list(serializer.errors)
            return Response(
                {
                    "status":200,
                    "error": error_list,
                }
            )
        

class Login(APIView):

    model= common_model.User
    serializer_class = common_serializer.LoginSerializer
    swagger_doc_item = swagger_doc.login_post

    @swagger_auto_schema(
        tags=swagger_doc_item['tag'],
        operation_id=swagger_doc_item['url_name'],
        operation_description=swagger_doc_item['description'],
        request_body=openapi.Schema(
            required=swagger_doc_item['required_fields'],
            type=openapi.TYPE_OBJECT,
            properties = swagger_doc_item['fields'],
        ),
        responses=swagger_doc_item['responses'],
        
    )

    def post(self, request):
        resp ={}
        serilizer = self.serializer_class(request.data)

        if serilizer.is_valid():
            email = serilizer.validated_data.get('email')
            password = serilizer.validate_data.get('password')

            try:
                user = self.model.objects.get(contact=email)

            except common_model.User.DoesNotExist:

                user = None
                return Response({"status":400,"error":["Login Failed..",]})

        if user.check_password(password):
            pass  # Credentials are valid
        else:
            user = None  # Incorrect password
    
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            resp['access_token']= str(token.key)
            resp['status']= 200
            resp['user']= common_serializer.UserSerializer(user).data
        else:
            resp['status']= 400
            resp['message']= "Login Failed or Account Not Found"
        
        return Response(resp)
    


class LogOut(APIView):

    swagger_doc_item = swagger_doc.logout_get

    @swagger_auto_schema(
        tags=swagger_doc_item['tag'],
        operation_id=swagger_doc_item['url_name'],
        operation_description=swagger_doc_item['description'],
        responses=swagger_doc_item['responses'],
        
    )

    def get(self, request):
        Token.objects.get_or_create(user= request.user).delete()
        return Response({
            "status":200,
            "message":"Logout Successful",
        })
    

class ForgetPassword(APIView):
    model= common_model.User
    serializer_class = common_serializer.ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if not serializer.is_valid():
            error_list = utils.serilalizer_error_list(serializer.errors)

            return Response({
                'status':400,
                'error':error_list,
            })
        

        try:
            user= self.model.objects.get(contact = request.data['contact'])
            user.otp = utils.get_rand_number(5)
            user.save()
            
            # send_forgot_password_link.delay(user.id, user.email, user.otp)
            background_thread = threading.Thread(target= tasks.send_forgot_password_link(args=(user.id, user.email, user.otp)))
            return Response({
                'status':200,
                'message':'An email has been sent to you..',
            })
            
        except Exception as e:
            print(e)
            return Response({
                'status':400,
                'error':['Account not found....'],
            })



class NewPassword(View):
    model= common_model.User
    form_class = forms.NewPasswordForm
    template = 'app_common/authentication/new_password.html'

    def get(self, request, encoded_user_id, otp):
        user_id = urlsafe_base64_decode(encoded_user_id).decode('utf-8')

        try:
            user = self.model.objects.get(id = user_id, otp = otp)
        except:
            messages.error(request, 'Something is wrong..')
            return redirect('app_common:new_password_set', encoded_user_id = encoded_user_id, otp = otp)

        context = {
            "form" : self.form_class,
            "email" : user.email,
        }
        return render(request, self.template, context)

    def post(self, request, encoded_user_id, otp):

        user_id = urlsafe_base64_decode(encoded_user_id).decode('utf-8')

        try:
            user = self.model.objects.get(id = user_id, otp = otp)
        except:
            messages.error(request, 'Something is wrong..')
            return redirect('app_common:new_password_set', encoded_user_id = encoded_user_id, otp = otp)

        form = self.form_class(request.POST)

        password = request.POST.get('password1')
        if form.is_valid():

            user.password = make_password(password)
            user.save()
            messages.success(request, 'Your Password is Changed sucessfully...')
        
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        return redirect('app_common:new_password_set', encoded_user_id = encoded_user_id, otp = otp)