from .Transactions import Transactions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.core.helper.helper import Helper

DEFAULT_LANG = "en"

# instantiate tansaction class

_transaction = Transactions()
_helper = Helper()

class getAllTransactions(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang):
        lang = DEFAULT_LANG if lang == None else lang
        response = _transaction.getAllTransactions(request, lang)
        return Response(response)
    
class getTransactionById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, lang, transactionid):
        lang = DEFAULT_LANG if lang == None else lang
        if not transactionid:
            return Response(
                {"message": "Incomplete data request!!!", "status": False},
                status=400
            )
        elif not _transaction.transactionExists(request, lang, transactionid):
            return Response(
                {"message": "Transaction does not Exist!!!", "status": False},
                status=400
            )
        else:
            # response
            response = _transaction.getTransactionById(request, lang, transactionid)
            return Response(response)
        
class registerTransaction(APIView):
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
            if not data["txnDate"]:
                return Response(
                    {"message": "Transaction Date is a required Field!!!", "status": False}
                )
            elif not data["event_id"]:
                return Response(
                    {"message": "Event is a required Field!!!", "status": False}
                )
            elif not data["member_id"]:
                return Response(
                    {"message": "Member is a required Flied!!!", "status": False}
                )
            elif not data["account_id"]:
                return Response(
                    {"message": "Account is a required Field!!!", "status": False}
                )
            elif not data["Amount"]:
                return Response(
                    {"message": "Amount", "status": False}
                )
            else:
                return Response(_transaction.registerTransaction(request, lang, userid, data))
                # return Response(
                #     {"message": "Transaction recorded Successfully!!", "status": True},
                #     status=201
                # )
        else:
            return Response(
                {
                    "message": "No data sumitted to the database!!!", "status": False
                }
            )
