from .models import EventLog,User
def WriteLog(uName, object_type, object_name, event_type,log_type):
    EVENT=EventLog()
    EVENT.user=User.objects.get(username=uName)
    EVENT.object_type=object_type
    EVENT.object_name=object_name
    EVENT.event_type=event_type
    EVENT.log_type=log_type
    EVENT.save()

