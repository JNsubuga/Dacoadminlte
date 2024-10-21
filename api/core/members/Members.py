from api.core.helper.helper import Helper
from api.models import *

from api.core.users.Users import Users
from api.core.locale.Locale import Locale


# master module class
class Members:
    def __init__(self):
        self.helper = Helper()
        self.users = Users()
        self.locale = Locale()
        self.events = Event()
        self.account = Account()

    def getAllMembers(self, request, lang):
        results = []
        members = Member.objects.filter(is_active=True).order_by("code")
        for member in members:
            member_item = {
                "id": member.pk,
                "names": member.names,
                "code": member.code,
                "phone_contact": member.phone_contact,
                "currentBalance": member.currentBalance,
                "created_by": self.users.getAuthUserById(request, lang, member.created_by_id),
                "created": member.created
            }
            results.append(member_item)
        return results
    
    def MemberExists(self, request, lang, memberid):
        return Member.objects.filter(pk=int(memberid)).exists()
    
    def getMemberById(self, request, lang, memberid):
        member = Member.objects.filter(pk=int(memberid)).get()
        return {
            "id": member.pk,
            "names": member.names,
            "code": member.code,
            "phone_contact": member.phone_contact,
            "currentBalance": member.currentBalance,
            "created_by": self.users.getAuthUserById(request, lang, member.created_by_id),
            # "created": member.created
        }
    
    def registerMember(self, request, lang, userid, data):
        member = Member.objects.create(
                names = data["names"],
                code = data["code"],
                phone_contact = data["phone_contact"],
                created_by_id=userid
        )
        member.save()
        return True
    
    def memberDetails(self, request, lang, memberid):
        results = []
        transactions = Transaction.objects.filter(pk=int(memberid)).get()
        for transaction in transactions:
            transaction_item = {
                "id": transaction.pk,
                "txnDate":transaction.txnDate,
                "event":self.events.getEventById(request, lang, transaction.event_id),
                "member":self.getMemberById(request, lang, transaction.member_id),
                "account": self.account.getAccountById(request, lang, transaction.account_id),
                "confirmed": transaction.confirmed,
                "Amount":transaction.Amount,
                "balanceBefore": transaction.balanceBefore,
                "created_by":self.users.getAuthUserById(request, lang, transaction.created_by_id),
                "created":transaction.created
            }
            results.append(transaction_item)
        return True
    
    def updateMemberCurrentBalance(self, request, lang, memberid, data_dic):
        # toUpdate = Member.objects.filter(pk=int(memberid)).update(data_dic)

        return data_dic
        # return True