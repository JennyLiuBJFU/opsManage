# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import  *

class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'asset_no', 'asset_type', 'organization', 'network_location', 'status',  'sn', 'idc'
                    ]

#
# # class ServerAdmin(admin.ModelAdmin):
#     list_display = ['asset_name', 'manage_ip','sub_asset_type', 'sn', 'os_type']
#
#     def asset_name(self, obj):
#         return obj.asset.asset_name
#
#     def sn(self, obj):
#        return obj.asset.sn
#
#     def manage_ip(self, obj):
#        return obj.asset.manage_ip
#
#
# class SecurityDeviceAdmin(admin.ModelAdmin):
#     list_display = ['asset_name', 'manage_ip', 'sub_asset_type', 'sn']
#
#     def asset_name(self, obj):
#         return obj.asset.asset_name
#
#     def sn(self, obj):
#         return obj.asset.sn
#
#     def manage_ip(self, obj):
#        return obj.asset.manage_ip
#
# class StorageDeviceDeviceAdmin(admin.ModelAdmin):
#     list_display = ['asset_name', 'manage_ip', 'sub_asset_type', 'sn']
#
#     def asset_name(self, obj):
#         return obj.asset.asset_name
#
#     def sn(self, obj):
#         return obj.asset.sn
#
#     def manage_ip(self, obj):
#        return obj.asset.manage_ip
#
# class NetworkDeviceDeviceAdmin(admin.ModelAdmin):
#     list_display = ['asset_name', 'manage_ip', 'sub_asset_type', 'sn']
#
#     def asset_name(self, obj):
#         return obj.asset.asset_name
#
#     def sn(self, obj):
#         return obj.asset.sn
#
#     def manage_ip(self, obj):
#        return obj.asset.manage_ip
#
# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ['parent_unit', 'name', 'memo']
#


#
# admin.site.register(Asset)
# admin.site.register(Server, ServerAdmin)
# admin.site.register(SecurityDevice,SecurityDeviceAdmin)
# admin.site.register(StorageDevice,StorageDeviceDeviceAdmin)
# admin.site.register(NetworkDevice,NetworkDeviceDeviceAdmin)
# admin.site.register(Software)
# admin.site.register(Idc)
# admin.site.register(Vendor)
# admin.site.register(Supplier)
# admin.site.register(Organization,OrganizationAdmin)
# admin.site.register(Contract)
# admin.site.register(Tag)
# admin.site.register(EventLog)





admin.site.register(Asset,AssetAdmin)
admin.site.register(Organization)
admin.site.register(Contract)
admin.site.register(Vendor)
admin.site.register(Supplier)
admin.site.register(Idc)
admin.site.register(Cabinet)
admin.site.register(CabinetSpace)
admin.site.register(Server)
admin.site.register(SecurityDevice)
admin.site.register(StorageDevice)
admin.site.register(NetworkDevice)
admin.site.register(Software)
admin.site.register(RAM)
admin.site.register(CPU)
admin.site.register(Disk)
admin.site.register(Port)
admin.site.register(Parts)
admin.site.register(EventLog)
admin.site.register(Device_model)

