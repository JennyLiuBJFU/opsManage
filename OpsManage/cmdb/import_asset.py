from .models import *
from .models import Asset
import xlrd
import qrcode
from django.contrib.auth.models import User



def import_server_info():
    # 1)从设备维护信息表中读出设备的IP地址、登陆帐号、密码、设备名称等信息
    workbook = xlrd.open_workbook("/home/kangz/PycharmProjects/opsManage/OpsManage/static/resources/server.xlsx")
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows

    for i in range(1, (rows)):
        asset_info = worksheet.row_values(i)
        newasset = Asset()
        newasset.asset_type='1'
        newasset.asset_name = asset_info[1]
        newasset.asset_no=asset_info[2]
        if asset_info[3] == '控制专网':
            newasset.network_location='1'
        elif asset_info[3] == '业务内网':
            newasset.network_location='2'
        elif asset_info[3] == '业务外网':
            newasset.network_location='3'
        Org=Organization.objects.get(org_name=asset_info[4])
        newasset.organization=Org
        if asset_info[5] == '使用中':
            newasset.status='1'
        elif asset_info[5] == '未使用':
            newasset.status='2'
        elif asset_info[5] == '故障':
            newasset.status='3'
        else:newasset.status='4'
        Model=Device_model.objects.get(models=asset_info[6])
        newasset.model=Model
        newasset.sn=asset_info[7]
        newasset.manage_ip=asset_info[8]
        USER=User.objects.get(username=asset_info[9])
        newasset.admin=USER
        newasset.idc=Idc.objects.get(idc_name=asset_info[10])
        newasset.cabinet=Cabinet.objects.get(cabinet_name=asset_info[11])
        newasset.cab_location=(newasset.cabinet.cabinet_height-int(asset_info[12]))*22+20
        newasset.height=int(asset_info[13])*22-2
        newasset.contract=Contract.objects.get(contract_name=asset_info[14])
        newasset.supplier=Supplier.objects.get(supplier_name=asset_info[15])
        print(asset_info[16])
        print(type(asset_info[16]))
        newasset.purchase_day=asset_info[16]
        newasset.expire_day=asset_info[17]
        newasset.approved_by=User.objects.get(username=asset_info[18])
        newasset.memo=asset_info[23]
        newasset.save()

        obj_url = "192.168.14.27/cmdb/detail" + str(newasset.id)
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=8,
                           border=2,
                           )
        qr.add_data(obj_url)
        qr.make(fit=True)
        img = qr.make_image()
        img_name = 'media/QRcode_imgs/' + newasset.asset_name + '.png'
        img.save(img_name)
        newasset.qrcode = img_name
        newasset.save()

        location=str(int(asset_info[12]))
        for i in range(0,int(asset_info[13])):
            CABSPACE=CabinetSpace.objects.get(cabinet=newasset.cabinet,cabinet_location=location)
            CABSPACE.asset=newasset
            CABSPACE.save()
            location=str(int(location)-1)

        newserver=Server()
        newserver.asset=newasset
        if asset_info[0] == 'PC服务器':
            newserver.sub_asset_type='1'
        elif asset_info[0] == '小型机':
            newserver.sub_asset_type='2'
        elif asset_info[0] == '刀片机':
            newserver.sub_asset_type='3'
        newserver.created_by='2'
        newserver.microcode=asset_info[19]
        if asset_info[20] == 'Windows':
            newserver.os_type='1'
        elif asset_info[20] == 'Unix':
            newserver.os_type='2'
        elif asset_info[20] == 'Linux':
            newserver.os_type='3'
        elif asset_info[20] == 'Other':
            newserver.os_type='4'
        newserver.os_distribution=asset_info[21]
        newserver.os_release=asset_info[22]
        newserver.save()
        print("successfully add "+newasset.asset_name)


def import_VM_info():
    # 1)从设备维护信息表中读出设备的IP地址、登陆帐号、密码、设备名称等信息
    workbook = xlrd.open_workbook("/home/kangz/PycharmProjects/opsManage/OpsManage/static/resources/VM.xlsx")
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows

    for i in range(1, (rows)):
        asset_info = worksheet.row_values(i)
        newasset = Asset()
        newasset.asset_type='1'
        newasset.asset_name = asset_info[1]
        newasset.asset_no=asset_info[2]
        if asset_info[3] == '控制专网':
            newasset.network_location='1'
        elif asset_info[3] == '业务内网':
            newasset.network_location='2'
        elif asset_info[3] == '业务外网':
            newasset.network_location='3'
        Org=Organization.objects.get(org_name=asset_info[4])
        newasset.organization=Org
        if asset_info[5] == '使用中':
            newasset.status='1'
        elif asset_info[5] == '未使用':
            newasset.status='2'
        elif asset_info[5] == '故障':
            newasset.status='3'
        else:newasset.status='4'
        Model=Device_model.objects.get(models=asset_info[6])
        newasset.model=Model
        newasset.sn=asset_info[7]
        newasset.manage_ip=asset_info[8]
        USER=User.objects.get(username=asset_info[9])
        newasset.admin=USER
        newasset.idc=Idc.objects.get(idc_name=asset_info[10])
        newasset.cabinet=Cabinet.objects.get(cabinet_name=asset_info[11])
        newasset.cab_location=(newasset.cabinet.cabinet_height-int(asset_info[12]))*22+20
        newasset.height=int(asset_info[13])*22-2
        newasset.contract=Contract.objects.get(contract_name=asset_info[14])
        newasset.supplier=Supplier.objects.get(supplier_name=asset_info[15])
        newasset.purchase_day=asset_info[16]
        newasset.expire_day=asset_info[17]
        newasset.approved_by=User.objects.get(username=asset_info[18])
        newasset.memo=asset_info[23]
        newasset.save()

        obj_url = "192.168.14.27/cmdb/detail" + str(newasset.id)
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=8,
                           border=2,
                           )
        qr.add_data(obj_url)
        qr.make(fit=True)
        img = qr.make_image()
        img_name = 'media/QRcode_imgs/' + newasset.asset_name + '.png'
        img.save(img_name)
        newasset.qrcode = img_name
        newasset.save()

        location=str(int(asset_info[12]))
        for i in range(0,int(asset_info[13])):
            CABSPACE=CabinetSpace.objects.get(cabinet=newasset.cabinet,cabinet_location=location)
            CABSPACE.asset=newasset
            CABSPACE.save()
            location=str(int(location)-1)

        newserver=Server()
        newserver.asset=newasset
        if asset_info[0] == '虚拟机':
            newserver.sub_asset_type='4'
        elif asset_info[0] == '容器':
            newserver.sub_asset_type='5'
        newserver.created_by='2'
        newserver.microcode=asset_info[19]
        if asset_info[20] == 'Windows':
            newserver.os_type='1'
        elif asset_info[20] == 'Unix':
            newserver.os_type='2'
        elif asset_info[20] == 'Linux':
            newserver.os_type='3'
        elif asset_info[20] == 'Other':
            newserver.os_type='4'
        newserver.os_distribution=asset_info[21]
        newserver.os_release=asset_info[22]
        ASSET=Asset.objects.get(asset_name=asset_info[24])
        SERVER=Server.objects.get(asset=ASSET)
        newserver.hosted_on=SERVER
        newserver.save()
        print("successfully add "+newasset.asset_name)



def import_otherDevice_info():
    # 1)从设备维护信息表中读出设备的IP地址、登陆帐号、密码、设备名称等信息
    workbook = xlrd.open_workbook("/home/kangz/PycharmProjects/opsManage/OpsManage/static/resources/otherDevice.xlsx")
    worksheet = workbook.sheet_by_index(0)
    rows = worksheet.nrows

    for i in range(1, (rows)):
        asset_info = worksheet.row_values(i)
        newasset = Asset()
        if asset_info[0]=='网络设备':
            newasset.asset_type='2'
        elif asset_info[0] == '安全设备':
            newasset.asset_type='3'
        elif asset_info[0] == '存储设备':
            newasset.asset_type='4'
        else: newasset.asset_type='5'
        newasset.asset_name = asset_info[2]
        newasset.asset_no=asset_info[3]
        if asset_info[4] == '控制专网':
            newasset.network_location='1'
        elif asset_info[4] == '业务内网':
            newasset.network_location='2'
        elif asset_info[4] == '业务外网':
            newasset.network_location='3'
        print(asset_info[5])
        print(type(asset_info[5]))
        Org=Organization.objects.get(org_name=asset_info[5])
        newasset.organization=Org
        if asset_info[6] == '使用中':
            newasset.status='1'
        elif asset_info[6] == '未使用':
            newasset.status='2'
        elif asset_info[6] == '故障':
            newasset.status='3'
        else:newasset.status='4'
        Model=Device_model.objects.get(models=asset_info[7])
        newasset.model=Model
        newasset.sn=asset_info[8]
        newasset.manage_ip=asset_info[9]
        USER=User.objects.get(username=asset_info[10])
        newasset.admin=USER
        newasset.idc=Idc.objects.get(idc_name=asset_info[11])
        newasset.cabinet=Cabinet.objects.get(cabinet_name=asset_info[12])
        newasset.cab_location=(newasset.cabinet.cabinet_height-int(asset_info[13]))*22+20
        newasset.height=int(asset_info[14])*22-2
        newasset.contract=Contract.objects.get(contract_name=asset_info[15])
        newasset.supplier=Supplier.objects.get(supplier_name=asset_info[16])
        newasset.purchase_day=asset_info[17]
        newasset.expire_day=asset_info[18]
        newasset.approved_by=User.objects.get(username=asset_info[19])
        newasset.memo=asset_info[20]
        newasset.save()

        obj_url = "192.168.14.27/cmdb/detail" + str(newasset.id)
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=8,
                           border=2,
                           )
        qr.add_data(obj_url)
        qr.make(fit=True)
        img = qr.make_image()
        img_name = 'media/QRcode_imgs/' + newasset.asset_name + '.png'
        img.save(img_name)
        newasset.qrcode = img_name
        newasset.save()

        location=str(int(asset_info[13]))
        for i in range(0,int(asset_info[14])):
            CABSPACE=CabinetSpace.objects.get(cabinet=newasset.cabinet,cabinet_location=location)
            CABSPACE.asset=newasset
            CABSPACE.save()
            location=str(int(location)-1)

        if asset_info[0]=='网络设备':
            newNetworkDevice=NetworkDevice()
            newNetworkDevice.asset=newasset
            if asset_info[1] == '路由器':
                newNetworkDevice.sub_asset_type='1'
            elif asset_info[1] == '交换机':
                newNetworkDevice.sub_asset_type='2'
            elif asset_info[1] =='工业交换机':
                newNetworkDevice.sub_asset_type='3'
            elif asset_info[1] =='无限控制器':
                newNetworkDevice.sub_asset_type='4'
            elif asset_info[1] == '无限AP':
                newNetworkDevice.sub_asset_type='5'
            newNetworkDevice.save()
        elif asset_info[0] == '安全设备':
            newSecurityDevice=SecurityDevice()
            newSecurityDevice.asset=newasset
            if asset_info[1] =='防火墙':
                newSecurityDevice.sub_asset_type='1'
            elif asset_info[1] =='入侵检测设备':
                newSecurityDevice.sub_asset_type='2'
            elif asset_info[1]=='入侵防御设备':
                newSecurityDevice.sub_asset_type='3'
            elif asset_info[1]=='综合安全网关':
                newSecurityDevice.sub_asset_type='4'
            elif asset_info[1]=='数据库审计系统':
                newSecurityDevice.sub_asset_type='5'
            elif asset_info[1] == '运维审计系统':
                newSecurityDevice.sub_asset_type='6'
            elif asset_info[1] == '防病毒网关':
                newSecurityDevice.sub_asset_type='7'
            elif asset_info[1]=='WAF防火墙':
                newSecurityDevice.sub_asset_type='8'
            elif asset_info[1] == '安全配置核查':
                newSecurityDevice.sub_asset_type='9'
            elif asset_info[1] == '网络准入系统':
                newSecurityDevice.sub_asset_type='10'
            elif asset_info[1] == '网闸设备':
                newSecurityDevice.sub_asset_type='11'
            elif asset_info[1]=='VPN设备':
                newSecurityDevice.sub_asset_type='12'
            newSecurityDevice.save()
        elif asset_info[0] == '存储设备':
            newStorageDevice=StorageDevice()
            newStorageDevice.asset=newasset
            if asset_info[1] == '磁盘阵列':
                newStorageDevice.sub_asset_type='1'
            elif asset_info[1]== '网络存储器':
                newStorageDevice.sub_asset_type='2'
            elif asset_info[1] == '光线交换机':
                newStorageDevice.sub_asset_type='3'
            elif asset_info[1] == '磁带库':
                newStorageDevice.sub_asset_type='4'
            elif asset_info[1] == '磁带机':
                newStorageDevice.sub_asset_type='5'
            newStorageDevice.save()

        print("successfully add "+newasset.asset_name)