from api.core.helper.helper import Helper
from api.models import *

from api.core.users.Users import Users
from api.core.locale.Locale import Locale
from api.core.accounts.Accounts import Accounts
from api.core.events.Events import Events
from api.core.members.Members import Members


# master module class
class Transactions:
    def __init__(self) -> None:
        self.helper = Helper()
        self.users = Users()
        self.locale = Locale()
        self.events = Events()
        self.members = Members()
        self.accounts = Accounts()

    def getAllTransactions(self, request, lang):
        results = []
        transactions = Transaction.objects.filter(confirmed=True).order_by("txnDate")
        for transaction in transactions:
            transaction_item = {
                "id": transaction.pk,
                "txnDate": transaction.txnDate,
                "event": self.events.getEventById(request, lang, transaction.event_id),
                "member": self.members.getMemberById(request, lang, transaction.member_id),
                "account": self.accounts.getAccountById(request, lang, transaction.account_id),
                "Amount": transaction.Amount,
                "balanceBefore": transaction.balanceBefore,
                "created_by": self.users.getAuthUserById(request, lang, transaction.created_by_id)
            }
            results.append(transaction_item)
        return results
    
    def transactionExists(self, request, lang, transactionid):
        return Transaction.objects.filter(pk=int(transactionid)).exists()
    
    def getTransactionById(self, request, lang, transactionid):
        transaction = Transaction.objects.filter(pk=int(transactionid)).get()
        return {
            "id": transaction.pk,
            "txnDate": transaction.txnDate,
            "event": self.events.getEventById(request, lang, transaction.event_id),
            "member": self.members.getMemberById(request, lang, transaction.member_id),
            "account": self.accounts.getAccountById(request, lang, transaction.account_id),
            "Amount": transaction.Amount,
            "balanceBefore": transaction.balanceBefore,
            "created_by": self.users.getAuthUserById(request, lang, transaction.created_by_id)
        }
    
    def registerTransaction(self, request, lang, userid, data):
        match data["event_id"]:
            case 2:
                return data["event_id"]
            case 3:
        # if data["event_id"] == 3:
                member = self.members.getMemberById(request, lang, data["member_id"])
                # toUpdate = Member.objects.filter(pk=int(data["member_id"]))
                # dbMemberToUpdate = toUpdate.get()

                # balanceBefore = dbMemberToUpdate.currentBalance
                balanceBefore = member["currentBalance"]
                balanceAfter = balanceBefore + data["Amount"]

                # transaction = Transaction.objects.create(
                #     txnDate = data["txnDate"],
                #     event_id = data["event_id"],
                #     member_id = data["member_id"],
                #     account_id = data["account_id"],
                #     Amount = data["Amount"],
                #     balanceBefore = balanceBefore,
                #     created_by_id = userid
                # )
                # transaction.save()
                updateRecord_dic = {
                    "names": member["names"],
                    "code": member["code"],
                    "phone_contact": member["phone_contact"],
                    "currentBalance": balanceAfter
                }
                
                recordToUpdate = self.members.updateMemberCurrentBalance(request, lang, member["id"], updateRecord_dic)
                # return member["currentBalance"]
                return recordToUpdate
                # return True

    def updateTransaction(self, request, lang, userid, transationid, data):
        return True