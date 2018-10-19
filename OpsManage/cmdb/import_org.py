from .models import Organization
import xlrd


def import_org_info():
    # 1)从设备维护信息表中读出设备的IP地址、登陆帐号、密码、设备名称等信息
    workbook = xlrd.open_workbook("/home/kangz/PycharmProjects/opsManage/OpsManage/static/resources/org.xlsx")
    worksheet = workbook.sheet_by_index(0)
    sheet_name = worksheet.name
    rows = worksheet.nrows

    for i in range(1, (rows)):
        org_info = worksheet.row_values(i)
        neworg = Organization()
        neworg.parent_org = Organization.objects.get(org_name=org_info[0])
        neworg.org_name = org_info[1]
        neworg.org_address = org_info[1]
        print(org_info[0], "--------", org_info[1])
        neworg.save()




