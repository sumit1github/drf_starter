from drf_yasg import openapi
  

sign_up_post = {
    'tag':["Authentication"],
    "url_name": "Sign Up",
    "required_fields" : ['full_name', 'email', 'contact', 'password','confirm_password'],
    "responses" : {201: 'Created', 400: 'Bad Request'},
    "description" : 'Sign Up',

    "fields" : {
        'full_name' : openapi.Schema(type=openapi.TYPE_STRING,max_length=50,description="Full name"),
        
        "email" : openapi.Schema(type=openapi.TYPE_STRING,format=openapi.FORMAT_EMAIL,description="Email."),

        "contact" : openapi.Schema(type=openapi.TYPE_NUMBER,max_length=15,description="<+country_code><Contact number> "),

        'password' : openapi.Schema(type=openapi.TYPE_STRING,max_length=50,description="Password"),

        'confirm_password' : openapi.Schema(type=openapi.TYPE_STRING,max_length=50,description="Confirm Password"),

    }
}

login_post = {
    'tag':["Authentication"],
    "url_name": "Login",
    "required_fields" : ['email','password',],
    "responses" : {200: 'Success', 400: 'Bad Request','access_token':'String'},
    "description" : 'Login',

    "fields" : {
        
        "email" : openapi.Schema(type=openapi.TYPE_STRING,format=openapi.FORMAT_EMAIL,description="Email."),
        'password' : openapi.Schema(type=openapi.TYPE_STRING,max_length=50,description="Password"),

    }
}

logout_get = {
    'tag':["Authentication"],
    "url_name": "LogOut",
    "required_fields" : [],
    "responses" : {200: 'Success', 400: 'Bad Request'},
    "description" : 'Logout',

    "fields" : {

    }
}