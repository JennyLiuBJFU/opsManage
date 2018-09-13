# -*- coding: utf-8 -*-
import json

import numpy
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from cmdb.models import *
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
    print('******************************')
    print(request.user)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    Assets = Asset.objects.all()
    Organizations=Organization.objects.all()
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Assets': Assets,
        'Organizations':Organizations
    }
    return render(request, 'cmdb/ServerManage/index.html', context)

@login_required()
def addARecord(request):
    Vendors = Vendor.objects.all()
    Organizations = Organization.objects.all()
    # Tags=Tag.objects.all()
    Users=User.objects.all()
    # IDCs=Idc.objects.all()
    Contracts=Contract.objects.all()
    Suppliers=Supplier.objects.all()
    Models=Device_model.objects.all()
    # Cabs=Cabinet.objects.all()
    # CabSpaces=CabinetSpace.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Vendors': Vendors,
        'Organizations': Organizations,
        # 'Tags':Tags,
        'Users':Users,
        # 'IDCs':IDCs,
        'Contracts':Contracts,
        'Suppliers':Suppliers,
        'Models':Models,
        # 'Cabs':Cabs,
        # 'CabSpaces':CabSpaces,
    }
    return render(request, 'cmdb/ServerManage/add/add.html', context)

def showIdcs(request):
    ORG=Organization.objects.get(id=request.GET['organization'])
    Idcs=Idc.objects.filter(organization=ORG)
    print(Idcs)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context={
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Idcs':Idcs,
    }
    return render(request, 'cmdb/ServerManage/add/add.html',context)

def showCabs(request):
    IDC=Idc.objects.get(id=request.GET['idc'])
    Cabs=Cabinet.objects.filter(idc=IDC)
    print(Cabs)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context={
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Cabs':Cabs,
    }
    return render(request, 'cmdb/ServerManage/add/add.html',context)

def showCabSpaces(request):
    CAB=Cabinet.objects.get(id=request.GET['cab'])
    CabSpaces=CabinetSpace.objects.filter(cabinet=CAB)
    CabSpacesRemain=CabSpaces.filter(asset=None)
    print(CabSpaces)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context={
        'USERNAME': str(request.user),
        'Perm': Perm,
        'CabSpaces':CabSpacesRemain,
    }
    return render(request, 'cmdb/ServerManage/add/add.html',context)

@login_required()
def addSubmit(request):

    print(request.POST)
    print(len(request.POST))

    ASSET=Asset()

    # text类型的8个
    ASSET.asset_name=request.POST['asset_name']
    ASSET.manage_ip=request.POST['manage_ip']
    ASSET.memo=request.POST['memo']
    ASSET.asset_no=request.POST['asset_no']
    ASSET.expire_day=request.POST['expire_day']
    ASSET.sn=request.POST['sn']
    # ASSET.model=request.POST['model']
    ASSET.purchase_day=request.POST['purchase_day']

    #直接select标签的3个
    if request.POST['status'] != "0":
        ASSET.status=request.POST['status']
    if request.POST['network_location'] !="0":
        ASSET.network_location = request.POST['network_location']
    if request.POST['asset_type']!="0":
        ASSET.asset_type = request.POST['asset_type']

    #外键的7个
    if request.POST['admin']!="0":
        ASSET.admin=User.objects.get(id=request.POST['admin'])
    if request.POST['model']!="0":
        ASSET.model = Device_model.objects.get(id=request.POST['model'])
    if request.POST['idc']!="0":
        ASSET.idc=Idc.objects.get(id=request.POST['idc'])
    if request.POST['contract']!="0":
        ASSET.contract=Contract.objects.get(id=request.POST['contract'])
    if request.POST['supplier']!="0":
        ASSET.supplier=Supplier.objects.get(id=request.POST['supplier'])
    if request.POST['organization']!="0":
        ASSET.organization=Organization.objects.get(id=request.POST['organization'])
    if request.POST['approved_by']!="0":
        ASSET.approved_by=User.objects.get(id=request.POST['approved_by'])
    if request.POST['cab']!="0":
        ASSET.cabinet=Cabinet.objects.get(id=request.POST['cab'])


    # #多对多1个
    ASSET.save()
    # tag_list=request.POST.getlist('tag','')
    # for t in tag_list:
    #     ASSET.tags.add(Tag.objects.get(id=t))
    # ASSET.save()

    CapSpasId=request.POST.getlist('cabSpace')
    for cId in CapSpasId:
        CABSPACE=CabinetSpace.objects.get(id=cId)
        CABSPACE.asset=ASSET
        CABSPACE.save()

    Assets = Asset.objects.all()
    Servers=Server.objects.all()
    print(Servers)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Assets': Assets,
        'ID':ASSET.id,
        'Servers':Servers,
    }
    if ASSET.asset_type=='1':
        return render(request,'cmdb/ServerManage/add/addOneToOne/addServer.html',context)
    elif ASSET.asset_type=='2':
        return render(request, 'cmdb/ServerManage/add/addOneToOne/addNetworkDevice.html', context)
    elif ASSET.asset_type=='3':
        return render(request, 'cmdb/ServerManage/add/addOneToOne/addSecurityDevice.html', context)
    elif ASSET.asset_type=='4':
        return render(request, 'cmdb/ServerManage/add/addOneToOne/addStorageDevice.html', context)
    else:
        return render(request, 'cmdb/ServerManage/index.html', context)

def editMore(request):
    ID=request.GET['assetId']
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus=CPU.objects.filter(asset=ASSET)
    disks=Disk.objects.filter(asset=ASSET)
    ports=Port.objects.filter(asset=ASSET)
    parts=Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context={
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'rams':rams,
        'cpus':cpus,
        'disks':disks,
        'ports':ports,
        'parts':parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def RAMSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    ram=RAM()
    ram.asset=ASSET
    ram.ram_model=request.POST['model']
    ram.ram_brand=request.POST['brand']
    ram.ram_volume=request.POST['volume']
    ram.ram_slot=request.POST['slot']
    ram.ram_status=request.POST['status']
    ram.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def RAMDelete(request):
    ID=request.GET['assetId']
    ram=RAM.objects.get(id=request.GET['ramId'])
    print(ram)
    ram.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def CPUSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    cpu=CPU()
    cpu.asset=ASSET
    cpu.cpu_model=request.POST['model']
    cpu.cpu_brand=request.POST['brand']
    cpu.cpu_speed=request.POST['speed']
    cpu.cpu_core_count=request.POST['core_count']
    cpu.cpu_slot=request.POST['slot']
    cpu.cpu_status=request.POST['status']
    cpu.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def CPUDelete(request):
    ID=request.GET['assetId']
    cpu=CPU.objects.get(id=request.GET['cpuId'])
    cpu.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def DiskSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    disk=Disk()
    disk.asset=ASSET
    disk.disk_name=request.POST['name']
    disk.disk_volume=request.POST['volume']
    disk.disk_model=request.POST['model']
    disk.disk_brand=request.POST['brand']
    disk.disk_serial=request.POST['serial']
    disk.disk_slot=request.POST['slot']
    disk.disk_status=request.POST['status']
    disk.disk_attr=request.POST['attr']
    disk.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def DiskDelete(request):
    ID=request.GET['assetId']
    disk=Disk.objects.get(id=request.GET['diskId'])
    disk.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def PortSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    port=Port()
    port.asset=ASSET
    port.port_type=request.POST['type']
    port.port_name=request.POST['name']
    port.port_slot=request.POST['slot']
    port.vlan=request.POST['vlan']
    port.ip=request.POST['ip']
    port.sub_ip=request.POST['sub_ip']
    port.mask=request.POST['mask']
    port.bandwidth=request.POST['bandwidth']
    port.status=request.POST['status']
    port.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def PortDelete(request):
    ID=request.GET['assetId']
    port=Port.objects.get(id=request.GET['portId'])
    port.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def PartSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    part=Parts()
    part.asset=ASSET
    part.parts_type=request.POST['type']
    part.parts_name=request.POST['name']
    part.parts_model=request.POST['model']
    part.parts_sn=request.POST['sn']
    part.parts_slot=request.POST['slot']
    part.parts_status=request.POST['status']
    part.memo=request.POST['partDesc']
    part.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def PartDelete(request):
    ID=request.GET['assetId']
    part=Parts.objects.get(id=request.GET['partId'])
    part.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def serverSubmit(request):
    print(request.POST)
    ASSET=Asset.objects.get(id=request.POST['assetId'])
    SERVER=Server()
    SERVER.asset=ASSET
    SERVER.created_by="2"
    if request.POST['hosted_on'] != '0':
        SERVER.hosted_on=Server.objects.get(id=request.POST['hosted_on'])
    if request.POST['sub_asset_type'] != '0':
        SERVER.sub_asset_type=request.POST['sub_asset_type']
    if request.POST['os_type'] != '0':
        SERVER.os_type = request.POST['os_type']
    SERVER.microcode=request.POST['microcode']
    SERVER.os_distribution=request.POST['os_distribution']
    SERVER.os_release=request.POST['os_release']
    SERVER.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations':Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def networkDeviceSubmit (request):
    print(request.POST)
    ASSET = Asset.objects.get(id=request.POST['assetId'])
    NETWORKDEVICE=NetworkDevice()
    NETWORKDEVICE.asset=ASSET
    if request.POST['sub_asset_type'] != '0':
        NETWORKDEVICE.sub_asset_type=request.POST['sub_asset_type']
    NETWORKDEVICE.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations':Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def storageDeviceSubmit(request):
    print(request.POST)
    ASSET = Asset.objects.get(id=request.POST['assetId'])
    STORAGEDEVICE = StorageDevice()
    STORAGEDEVICE.asset = ASSET
    if request.POST['sub_asset_type'] != '0':
        STORAGEDEVICE.sub_asset_type = request.POST['sub_asset_type']
    STORAGEDEVICE.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def securityDeviceSubmit(request):
    print(request.POST)
    ASSET = Asset.objects.get(id=request.POST['assetId'])
    SECURITYDEVICE = SecurityDevice()
    SECURITYDEVICE.asset = ASSET
    if request.POST['sub_asset_type'] != '0':
        SECURITYDEVICE.sub_asset_type = request.POST['sub_asset_type']
    SECURITYDEVICE.memo=request.POST['memo']
    SECURITYDEVICE.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

def detail(request, v):
    print(request)
    ASSET = Asset.objects.get(id=v)

    # 组装机柜空间
    SpaceList = []
    for i in ASSET.cabinetspace_set.values_list():
        SpaceList.append(int(i[3]))

    if len(SpaceList) >= 2:
        max = str(numpy.max(SpaceList))
        min = str(numpy.min(SpaceList))
        CabinetSpace = min +'U' + '--' + max + 'U'
    elif len(SpaceList) == 1:
        CabinetSpace = str(SpaceList[0]) + 'U'
    else:
        CabinetSpace = None

    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ASSET': ASSET,
        'CabinetSpace': CabinetSpace,
    }
    return render(request, 'cmdb/detail.html', context)


@login_required()
def editModel(request):
    # 判断是否有删除请求，有则删除厂商
    dmodel = request.POST.getlist('delete_model')
    if len(dmodel):
        for i in dmodel:

            Device_model.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    model = Device_model.objects.all()
    vendors = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'model': model,
        'vendors':vendors
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editModel.html', context)

@login_required()
def addModelSubmit(request):
    o = Device_model()
    o.img=request.FILES.get('image')
    # o.vendor=request.POST['telephone']
    o.models=request.POST['models']
    o.save()
    model = Device_model.objects.all()
    vendors = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'model': model,
        'vendors':vendors,
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editModel.html', context)

@login_required()
def editOrganization(request):
    # 判断是否有删除请求，有则删除厂商
    dorg = request.POST.getlist('delete_org')
    print(dorg)
    if len(dorg):
        for i in dorg:
           Organization.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    org = Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'org': org
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editOrganization.html',context)

@login_required()
def addOrgSubmit(request):
    o = Organization()
    o.org_name=request.POST['name']
    o.org_address = request.POST['address']
    o.org_memo=request.POST['memo']
    o.save()
    org = Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'org': org
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editOrganization.html', context)

def editVendor(request):
    # 判断是否有删除请求，有则删除厂商
    dvendor = request.POST.getlist('delete_vendor')
    print(dvendor)
    if len(dvendor):
        for i in dvendor:
           Vendor.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    vendor = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'vendor': vendor,
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editVendor.html',context)

@login_required()
def addVendorSubmit(request):
    o = Vendor()
    o.vendor_name=request.POST['name']
    o.vendor_phone=request.POST['phone']
    o.vendor_memo=request.POST['memo']
    o.save()
    vendor = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'vendor': vendor
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editVendor.html', context)

@login_required()
def editIdc(request):
    # 判断是否有删除请求，有则删除厂商
    didc = request.POST.getlist('delete_idc')
    if len(didc):
        for i in didc:
            Idc.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    idc = Idc.objects.all()
    orgs = Organization.objects.all()
    print(orgs)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'idc': idc,
        'orgs':orgs,
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editIdc.html',context)

@login_required()
def addIdcSubmit(request):
    print(request.POST)
    o = Idc()
    o.name=request.POST['name']
    o.address=request.POST['address']
    o.memo=request.POST['memo']
    o.save()
    idc = Idc.objects.all()
    orgs = Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'idc': idc,
        'orgs': orgs,
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editIdc.html', context)

@login_required()
def editContract(request):
    # 判断是否有删除请求，有则删除厂商
    dcontract = request.POST.getlist('delete_contract')
    if len(dcontract):
        for i in dcontract:
            Contract.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    contract = Contract.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'contract': contract
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editContract.html',context)

@login_required()
def addContractSubmit(request):
    o = Contract()
    o.contract_number=request.POST['number']
    o.contract_name=request.POST['name']
    o.contract_content=request.POST['content']
    o.contract_memo=request.POST['memo']
    o.save()
    contract = Contract.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'contract': contract
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editContract.html', context)

@login_required()
def editSupplier(request):
    # 判断是否有删除请求，有则删除厂商
    dsupplier = request.POST.getlist('delete_supplier')
    if len(dsupplier):
        for i in dsupplier:
            Supplier.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    supplier = Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'supplier': supplier
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editSupplier.html',context)

@login_required()
def addSupplierSubmit(request):
    o = Supplier()
    o.supplier_name = request.POST['name']
    o.supplier_contacts = request.POST['contact']
    o.supplier_phone = request.POST['phone']
    o.supplier_memo = request.POST['memo']
    o.save()
    supplier = Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'supplier': supplier
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editSupplier.html', context)

@login_required()
def deleteARecord(request):
    v = request.GET['myid']
    Asset.objects.get(id=v).delete()
    Assets = Asset.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Assets':Assets,
    }
    return render(request, 'cmdb/ServerManage/index.html', context)

@login_required()
def editARecord(request):
    v = request.GET['myid']
    ASSET=Asset.objects.get(id=v)
    Vendors = Vendor.objects.all()
    Organizations = Organization.objects.all()
    # Tags = Tag.objects.all()
    Users = User.objects.all()
    IDCs = Idc.objects.filter(organization=ASSET.organization)
    Cabinets=Cabinet.objects.filter(idc=ASSET.idc)
    CabSpaces=CabinetSpace.objects.filter(cabinet=ASSET.cabinet,asset=None)
    CSSelected=CabinetSpace.objects.filter(asset=ASSET)
    print("!!!!!!!!!!!!!!!!!!!!!!!")
    print(CSSelected)
    Contracts = Contract.objects.all()
    Suppliers = Supplier.objects.all()
    Servers=Server.objects.all()
    Models=Device_model.objects.all()

    PURCHASE_DAY=str(ASSET.purchase_day)
    EXPIRE_DAY=str(ASSET.expire_day)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Models':Models,
        'Cabinets':Cabinets,
        'CabSpaces':CabSpaces,
        'CSSelected':CSSelected,
        'Vendors': Vendors,
        'Organizations': Organizations,
        # 'Tags': Tags,
        'Users': Users,
        'IDCs': IDCs,
        'Contracts': Contracts,
        'Suppliers': Suppliers,
        'ASSET': ASSET,
        'ID':v,
        'PURCHASE_DAY':PURCHASE_DAY,
        'EXPIRE_DAY':EXPIRE_DAY,
        'Servers':Servers,
    }
    return render(request, 'cmdb/ServerManage/edit/editARecord.html', context)

@login_required()
def editSubmit(request):

    print(request.POST)
    print(len(request.POST))

    ASSET=Asset.objects.get(id=request.GET['myid'])

    print(ASSET.id)
    # text类型的8个
    ASSET.asset_name = request.POST['asset_name']
    ASSET.manage_ip = request.POST['manage_ip']
    ASSET.memo = request.POST['memo']
    ASSET.asset_no = request.POST['asset_no']
    ASSET.expire_day = request.POST['expire_day']
    ASSET.sn = request.POST['sn']
    # ASSET.model = request.POST['model']
    ASSET.purchase_day = request.POST['purchase_day']

    # 直接select标签的3个
    if request.POST['status']!="0":
        ASSET.status = request.POST['status']
    if request.POST['network_location']!="0":
        ASSET.network_location = request.POST['network_location']
    if request.POST['asset_type']!="0":
        ASSET.asset_type = request.POST['asset_type']

    # 外键的7个
    if request.POST['admin']!="0":
        ASSET.admin = User.objects.get(id=request.POST['admin'])
    if request.POST['model']!="0":
        ASSET.model=Device_model.objects.get(id=request.POST['model'])
    # ASSET.vendor = Vendor.objects.get(id=request.POST['vendor'])
    if request.POST['organization']:
        ASSET.organization = Organization.objects.get(id=request.POST['organization'])
    if request.POST['idc']!="0":
        ASSET.idc = Idc.objects.get(id=request.POST['idc'])
    if request.POST['cab'] !="0":
        ASSET.cabinet = Cabinet.objects.get(id=request.POST['cab'])
    if request.POST['contract']!="0":
        ASSET.contract = Contract.objects.get(id=request.POST['contract'])
    if request.POST['supplier']!="0":
        ASSET.supplier = Supplier.objects.get(id=request.POST['supplier'])
    if request.POST['approved_by']!="0":
        ASSET.approved_by = User.objects.get(id=request.POST['approved_by'])

    # 多对多1个，目前未考虑，暂时按照外键处理
    ASSET.save()
    # tag_list = request.POST.getlist('tag', '')
    # for t in tag_list:
    #     ASSET.tags.add(Tag.objects.get(id=t))
    # ASSET.save()

    CSSelected=CabinetSpace.objects.filter(asset=ASSET)
    for css in CSSelected:
        print("******************************")
        print(css)
        css.asset= None
        print(css)
        css.save()

    CapSpasId = request.POST.getlist('cabSpace')
    for cId in CapSpasId:
        CABSPACE = CabinetSpace.objects.get(id=cId)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(CABSPACE)
        CABSPACE.asset = ASSET
        CABSPACE.save()



    if ASSET.asset_type=="1" :
        if Server.objects.filter(asset=ASSET):
            SERVER=Server.objects.get(asset=ASSET)
        else:
            SERVER=Server()
            SERVER.asset=ASSET
        SERVER.sub_asset_type=request.POST['sub_asset_type']
        if request.POST['hosted_on'] != '0':
            SERVER.hosted_on = Server.objects.get(id=request.POST['hosted_on'])
        SERVER.microcode=request.POST['microcode']
        SERVER.sub_asset_type = request.POST['sub_asset_type']
        SERVER.os_type = request.POST['os_type']
        SERVER.os_distribution = request.POST['os_distribution']
        SERVER.os_release = request.POST['os_release']
        SERVER.save()
    elif ASSET.asset_type=="2":
        if NetworkDevice.objects.filter(asset=ASSET):
            NETWORKDEVICE=NetworkDevice.objects.get(asset=ASSET)
        else:
            NETWORKDEVICE=NetworkDevice()
            NETWORKDEVICE.asset=ASSET
        NETWORKDEVICE.sub_asset_type = request.POST['sub_asset_type']
        NETWORKDEVICE.save()
    elif ASSET.asset_type == "3":
        if SecurityDevice.objects.filter(asset=ASSET):
            SECURITYDEVICE = SecurityDevice.objects.get(asset=ASSET)
        else:
            SECURITYDEVICE=SecurityDevice()
            SECURITYDEVICE.asset=ASSET
        SECURITYDEVICE.sub_asset_type = request.POST['sub_asset_type']
        SECURITYDEVICE.memo=request.POST['SeDMemo']
        SECURITYDEVICE.save()
    elif ASSET.asset_type=="4":
        if StorageDevice.objects.filter(asset=ASSET):
            STORAGEDEVICE = StorageDevice.objects.get(asset=ASSET)
        else:
            STORAGEDEVICE=StorageDevice()
            STORAGEDEVICE.asset=ASSET
        STORAGEDEVICE.sub_asset_type = request.POST['sub_asset_type']
        STORAGEDEVICE.save()

    Assets = Asset.objects.all()
    Organizations=Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Assets': Assets,
        'Organizations': Organizations
    }
    return render(request, 'cmdb/ServerManage/index.html', context)


def filter(request):

    typeID=request.GET['myType']
    orgID=request.GET['myOrg']

    if (typeID == "0" and orgID == "0"):
        ASSET = Asset.objects.all()
    elif (typeID != "0" and orgID == "0"):
        ASSET = Asset.objects.filter(asset_type=request.GET['myType'])

    elif (typeID == "0" and orgID != "0"):
        ASSET = Asset.objects.filter(organization=request.GET['myOrg'])

    else:
        ASSET = Asset.objects.filter(organization=request.GET['myOrg'],asset_type=request.GET['myType'])
    Organizations = Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Assets': ASSET,
        'Organizations':Organizations,
        'TYPE':typeID,
        'ORG':orgID,
    }
    return render(request, 'cmdb/ServerManage/index.html', context)

def basicData(request):
    return render(request,'cmdb/basicData/index.html')