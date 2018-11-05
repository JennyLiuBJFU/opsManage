# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^asset/$',views.asset,name="asset"),
    url(r'^addARecord$', views.addARecord),
    url(r'^serverSubmit$', views.serverSubmit),
    url(r'^networkDeviceSubmit', views.networkDeviceSubmit),
    url(r'^storageDeviceSubmit', views.storageDeviceSubmit),
    url(r'^securityDeviceSubmit', views.securityDeviceSubmit),
    url(r'^addSubmit$', views.addSubmit),
    url(r'^editModel$', views.editModel),
    url(r'^editVendor$', views.editVendor),
    url(r'^editSupplier$', views.editSupplier),
    url(r'^detail(\d+)', views.detail, name='asset_detail'),
    url(r'^deleteARecord$', views.deleteARecord),
    url(r'^editARecord$', views.editARecord),
    url(r'^editSubmit$', views.editSubmit),
    url(r'^addModelSubmit$', views.addModelSubmit),
    url(r'^addVendorSubmit$', views.addVendorSubmit),
    url(r'^addSupplierSubmit$', views.addSupplierSubmit),
    url(r'^showCabs', views.showcabs, name="showCabs"),
    url(r'^showIdcs', views.showidcs, name="showIdcs"),
    url(r'^showCabSpaces', views.showcabspace, name="showcabspace"),
    url(r'^editMore', views.editMore),
    url(r'^RAMSubmit', views.RAMSubmit),
    url(r'^CPUSubmit', views.CPUSubmit),
    url(r'^DiskSubmit', views.DiskSubmit),
    url(r'^PortSubmit', views.PortSubmit),
    url(r'^PartSubmit', views.PartSubmit),
    url(r'^RAMDelete', views.RAMDelete),
    url(r'^CPUDelete', views.CPUDelete),
    url(r'^DiskDelete', views.DiskDelete),
    url(r'^PortDelete', views.PortDelete),
    url(r'^PartDelete', views.PartDelete),
    url(r'^basicData', views.orgManage),
    url(r'^editCab', views.editCab),
    url(r'^addCabSubmit', views.addCabSubmit),
    url(r'^addIdc', views.addIdc),
    url(r'^idcSubmit', views.idcSubmit),
    url(r'^editIdc', views.editIdc),
    url(r'^submitIdcEdit', views.submitIdcEdit),
    url(r'^deleteAIdc', views.deleteAIdc),
    url(r'^cabDetail', views.cabDetail),
    url(r'^idcManage',views.idcManage),
    # url(r'^userManage',views.userManage),
    # url(r'addUserSubmit',views.addUserSubmit),
    url(r'^contractManage',views.contractManage),
    url(r'^addContractSubmit',views.addContractSubmit),
    url(r'^orgManage',views.orgManage),
    url(r'^editOrg',views.editOrg),
    url(r'^addOrgSubmit',views.addOrgSubmit),
    url(r'^supplierManage',views.supplierManage),
    url(r'^addSupplierSubmitM',views.addSupplierSubmitM),
    url(r'^vendorManage',views.vendorManage),
    url(r'^addVendorSubmitM',views.addVendorSubmitM),
    url(r'^assetMap',views.assetMap, name='assetMap'),
    url(r'^asset_subtype(\d+)/$', views.subtype),
    url(r'^device_model(\d+)/$', views.devicemodel),
    url(r'^showidcs(\d+)/$', views.showidcs),
    url(r'^showcabs(\d+)/$', views.showcabs),
    url(r'^showcabspace(\d+)/$', views.showcabspace),

    # url(r'^editAdminSubmit',views.editAdminSubmit),
    url(r'^editSupplierSubmit$',views.editASupplierSubmit),
    url(r'^editSupplierSubmitM',views.editASupplierSubmitM),
    url(r'^editContractSubmit',views.editContractSubmit),
    url(r'^editACabinetSubmit',views.editACabinetSubmit),
    url(r'^editAOrganizationSubmit',views.editAOrganizationSubmit),
    url(r'^editVendorSubmit',views.editVendorSubmit),
    url(r'^importorg/',views.importorg),
    url(r'editModelSubmit',views.editModelSubmit),

    url(r'modelManage',views.modelManage),
    url(r'^addAModelSubmit',views.addAModelSubmit),
    url(r'^editAModelSubmit',views.editAModelSubmit),
    url(r'^editAVendorSubmit',views.editAVendorSubmit),

    url(r'^doVerify',views.doVerify),
    # url(r'userVerify',views.userVerify),

]