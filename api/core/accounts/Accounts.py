from api.core.helper.helper import Helper
from api.models import *

from api.core.users.Users import Users
from api.core.locale.Locale import Locale


# master module class
class Accounts:
    def __init__(self):
        self.helper = Helper()
        self.users = Users()
        self.locale = Locale()
        self.events = Event()
        self.members = Member()

    def getAllAccounts(self, request, lang):
        results = []
        accounts = Account.objects.filter(is_disabled=False).order_by("accountYear","code")
        for account in accounts:
            account_item = {
                "id": account.pk,
                "name": account.name,
                "accountYear": account.accountYear,
                "code": account.code,
                "anualPrinciple": account.anualPrinciple,
                "created_by": self.users.getAuthUserById(request, lang, account.created_by_id),
                # "created": account.created
            }
            results.append(account_item)
        return results
    
    def AccountExists(self, request, lang, accountid):
        return Account.objects.filter(pk=int(accountid)).exists()
    
    def getAccountById(self, request, lang, accountid):
        account = Account.objects.filter(pk=int(accountid)).get()
        return {
            "id": account.pk,
            "name": account.name,
            "accountYear": account.accountYear,
            "code": account.code,
            "anualPrinciple": account.anualPrinciple,
            "created_by": self.users.getAuthUserById(request, lang, account.created_by_id),
            # "created": account.created 
        }
    
    def createAccount(self, request, userid, data):
        account = Account.objects.create(
            name=data["name"],
            accountYear=data["accountYear"],
            code=data["code"],
            anualPrinciple=data["anualPrinciple"],
            # created_by=User(pk=int(data["created_by_id"]))
            created_by_id=userid
        )
        account.save()
        return True
    
    def accountDetails(self, request, lang, accountid):
        results = []
        transactions = Transaction.objects.filter(pk=int(accountid)).get()
        for transaction in transactions:
            transaction_item = {
                "id": transaction.pk,
                "txnDate":transaction.txnDate,
                "event":self.events.getEventById(request, lang, transaction.event_id),
                "member":self.member.getMemberById(request, lang, transaction.member_id),
                "account": self.getAccountById(request, lang, transaction.account_id),
                "confirmed": transaction.confirmed,
                "Amount":transaction.Amount,
                "balanceBefore": transaction.balanceBefore,
                "created_by":self.users.getAuthUserById(request, lang, transaction.created_by_id),
                "created":transaction.created
            }
            results.append(transaction_item)
        return True