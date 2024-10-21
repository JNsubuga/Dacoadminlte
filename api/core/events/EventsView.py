from .Events import Events
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.core.helper.helper import Helper

DEFAULT_LANG = "en"

# instantiate event class

_event = Events()
_helper = Helper()

class getAllEvents(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _event.getAllEvents(request, lang)
        return Response(response)
    
class getEventById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, eventid):
        lang = DEFAULT_LANG if lang == None else lang
        if not eventid:
            return Response(
                {"message": "Incomplete data request!!!", "status": False},
                status=400
            )
        elif not _event.eventExists(request, lang, eventid):
            return Response(
                {
                    "message": "Event does not Exist!!!",
                    "status": False
                }, status=400
            )
        else:
            response = _event.getEventById(request, lang, eventid)
            return Response(response)

class createEvent(APIView):
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
            if not data["event"]:
                return Response(
                    {"message": "Event is a required Feild!!!", "status": False}
                )
            else:
                _event.createEvent(request, lang, userid, data)
                return Response(
                    {"message": "Event created Successfully!!", "status": True}, status=201
                )
        else:
            return Response(
                {"message":"No data submitted to the database!!!","status": False}
            )
