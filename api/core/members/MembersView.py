from .Members import Members
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.core.helper.helper import Helper

DEFAULT_LANG = "en"

# instantiate member class

_member = Members()
_helper = Helper()

class getAllMembers(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _member.getAllMembers(request, lang)
        return Response(response)
    
class getMemberById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, memberid):
        lang = DEFAULT_LANG if lang == None else lang
        if not memberid:
            return Response(
                {
                    "message": "Incomplete data request!!!", "status": False
                }, status=400
            )
        elif not _member.MemberExists(request, lang, memberid):
            return Response(
                {"message": "Member does not Exist!!!", "status": False}, status=400
            )
        # response
        response = _member.getMemberById(request, lang, memberid)
        return Response(response)
    
class registerMember(APIView):
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
            if not data["names"]:
                return Response(
                    {"message": "Names is a required field!!!", "status": False}
                )
            elif not data["code"]:
                return Response(
                    {"message": "Code is a required field!!!", "status": False}
                )
            elif not data["phone_contact"]:
                return Response(
                    {
                        "message": "Phone_contact is required field!!!", "status": False
                    }
                )
            else:
                _member.registerMember(request, lang, userid, data)
                return Response(
                    {
                        "message": "Member is registered Successfully!!", "status": True
                    }, status=201
                )
        else:
            return Response(
                {
                    "message": "No data submitted to the database!!!", "status": False
                }
            )