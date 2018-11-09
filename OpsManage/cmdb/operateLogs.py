from .models import EventLog,User,Asset

def WriteLog(uName, object_type, object_name,toAssetId, event_type):
    EVENT=EventLog()
    EVENT.user=User.objects.get(username=uName)
    EVENT.object_type=object_type
    EVENT.object_name=object_name
    EVENT.event_type=event_type
    if toAssetId != '0':
        EVENT.toAsset=Asset.objects.get(id=toAssetId)
    EVENT.save()

