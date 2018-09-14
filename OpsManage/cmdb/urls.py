# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
                # url(r'^$', views.index, name='asset'),
                # url(r'^detail(\d+)', views.detail, name='asset_detail'),
                # url(r'^filter', views.filter, name="filter"),
url(r'^$', views.index),
    url(r'^addARecord$',views.addARecord),
    url(r'^serverSubmit$',views.serverSubmit),
    url(r'^networkDeviceSubmit',views.networkDeviceSubmit),
    url(r'^storageDeviceSubmit',views.storageDeviceSubmit),
    url(r'^securityDeviceSubmit',views.securityDeviceSubmit),
    url(r'^filter',views.filter,name="filter"),
    url(r'^addSubmit$', views.addSubmit),
    url(r'^editModel$',views.editModel),
    url(r'^editVendor$',views.editVendor),
    url(r'^editOrganization$', views.editOrganization),
    url(r'^editIdc$', views.editIdc),
    url(r'^editContract$', views.editContract),
    url(r'^editSupplier$', views.editSupplier),
    url(r'^detail(\d+)', views.detail, name='asset_detail'),
    url(r'^deleteARecord$',views.deleteARecord),
    url(r'^editARecord$',views.editARecord),
    url(r'^editSubmit$', views.editSubmit),
    url(r'^addModelSubmit$', views.addModelSubmit),
    url(r'^addOrgSubmit$', views.addOrgSubmit),
    url(r'^addVendorSubmit$', views.addVendorSubmit),
    url(r'^addIdcSubmit$', views.addIdcSubmit),
    url(r'^addContractSubmit$', views.addContractSubmit),
    url(r'^addSupplierSubmit$', views.addSupplierSubmit),
    url(r'^showCabs', views.showCabs, name="showCabs"),
    url(r'^showIdcs', views.showIdcs, name="showIdcs"),
    url(r'^showCabSpaces', views.showCabSpaces, name="showCabSpaces"),
    # url(r'^moreInfo', views.moreInfo),
    url(r'^editMore',views.editMore),
    url(r'^RAMSubmit',views.RAMSubmit),
    url(r'^CPUSubmit',views.CPUSubmit),
    url(r'^DiskSubmit',views.DiskSubmit),
    url(r'^PortSubmit',views.PortSubmit),
    url(r'^PartSubmit',views.PartSubmit),
    url(r'^RAMDelete',views.RAMDelete),
    url(r'^CPUDelete',views.CPUDelete),
    url(r'^DiskDelete', views.DiskDelete),
    url(r'^PortDelete', views.PortDelete),
    url(r'^PartDelete', views.PartDelete),
    url(r'^basicData',views.basicData),
    url(r'^editCab',views.editCab),
    url(r'^addCabSubmit',views.addCabSubmit),
              ]
