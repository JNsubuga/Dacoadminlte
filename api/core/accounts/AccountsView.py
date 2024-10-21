from .Accounts import Accounts
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.core.helper.helper import Helper

DEFAULT_LANG = "en"

# instantiate account class

_account = Accounts()
_helper = Helper()


class getAllAccounts(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _account.getAllAccounts(request, lang)
        return Response(response)
    
class getAccountById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, accountid):
        lang = DEFAULT_LANG if lang == None else lang
        if not accountid:
            return Response(
                {"message": "Incomplete data request!!!", "status": False},
                status=400
            )
        elif not _account.AccountExists(request, lang, accountid):
            return Response(
                {
                    "message": "Account does not Exist!!!",
                    "status": False
                }, 
                status=400
            )
        # response
        response = _account.getAccountById(request, lang, accountid)
        return Response(response)
    
class createAccount(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        data = request.data  
        #############################################
        token_auth = _helper.getAuthToken(request)
        if not token_auth["status"]:
            return Response(
                token_auth,
                status=400
            )
        token = token_auth["token"]
        userid = Token.objects.get(key=token).user_id
        if len(data) > 0:
            if not data["name"]:
                return Response(
                    {
                        "message": "Name is a required field!!!", "status": False   
                    }
                )
            elif not data["accountYear"]:
                return Response(
                    {
                        "message": "Account Year is a required field!!!", "status": False   
                    }
                )
            elif not data["code"]:
                return Response(
                    {
                        "message": "code is a required field!!!", "status": False   
                    }
                )
            elif not data["anualPrinciple"]:
                return Response(
                    {
                        "message": "Annual Principle is a required field!!!", "status": False   
                    }
                )
            else:
                _account.createAccount(request, userid, data)
                return Response(
                    {
                        "message": "Account created Successfully!!", "status": True
                    }, status=201
                )
        else:
            return Response(
                {
                    "message": "No data submited to the database!!!", "status": False
                }
            )