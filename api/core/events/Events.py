from  api.core.helper.helper import Helper
from api.models import *

from api.core.users.Users import Users
from api.core.locale.Locale import Locale


# master module class
class Events:
    def __init__(self):
        self.helper = Helper()
        self.users = Users()
        self.locale = Locale()

    def getAllEvents(self, request, lang):
        results = []
        events = Event.objects.all()
        for event in events:
            event_item = {
                "id": event.pk,
                "event": event.event,
                "created_by": self.users.getAuthUserById(request, lang, event.created_by_id)
            }
            results.append(event_item)
        return results
    
    def eventExists(self, request, lang, eventid):
        return Event.objects.filter(pk=int(eventid)).exists()

    def getEventById(self, request, lang, eventid):
        event = Event.objects.filter(pk=int(eventid)).get()
        return{
            "id": event.pk,
            "event": event.event,
            "created_by": self.users.getAuthUserById(request, lang, event.created_by_id)
        }

    def createEvent(self, request, lang, userid, data):
        event = Event.objects.create(
            event = data["event"],
            created_by_id = userid
        )
        event.save()
        return True
