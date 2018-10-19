# _#_ coding:utf-8 _*_

# import magic
from ..cmdb.models import Organization


def Org_Data_create():
    orglist = Organization.objects.all()

    # ------树形图数据计算，排出各单位及其子单位的列表--------
    zxj = Organization.objects.get(org_name="中线局")
    zxj_context = []

    # 查询分局局对象
    fenju_list = Organization.objects.filter(parent_org=zxj.id)

    # 逐级生成各级组织名称
    for fenju in fenju_list:
        guanlichu_list = Organization.objects.filter(parent_org=fenju.id)
        fenju_name = fenju.org_name
        list_tmp = []
        for guanlichu in guanlichu_list:
            xiandizhan_list = Organization.objects.filter(parent_org=guanlichu.id)
            guanlichu_name = guanlichu.org_name
            xdz_list = []
            for xiandizhan in xiandizhan_list:
                xdz_context = {str(xiandizhan.id): xiandizhan.org_name}
                xdz_list.append(xdz_context)
            glc_context = {str(guanlichu.id): guanlichu_name, 'children': xdz_list}
            list_tmp.append(glc_context)
        fenju_context = {str(fenju.id): fenju_name, "children": list_tmp}
        zxj_context.append(fenju_context)

    print("^^^^^^^^^^^^^^^^^^^^^^^^")
    print(zxj_context)
    return zxj_context


"""
数据格式
a = [
    {'-1': '中线局局机关'},
    {'2': '河北分局', 'children': [{'3': '邯郸管理处', 'children': [{'11': '邯郸现地站1'},{'12': '邯郸现地站2'}]},{'5': '石家庄管理处', 'children': [{'17': '石家庄县地站1'},{'17': '石家庄县地站2'}]}]},
    ]
"""


def Org_Data_create11():
    orglist = Organization.objects.all()

    # ------树形图数据计算，排出各单位及其子单位的列表--------
    zxj = Organization.objects.get(org_name="中线局")
    zxj_context = []

    # 查询分局局对象
    fenju_list = Organization.objects.filter(parent_org=zxj.id)

    # 逐级生成各级组织名称
    for fenju in fenju_list:
        guanlichu_list = Organization.objects.filter(parent_org=fenju.id)
        fenju_name = fenju.org_name
        list_tmp = []
        for guanlichu in guanlichu_list:
            xiandizhan_list = Organization.objects.filter(parent_org=guanlichu.id)
            guanlichu_name = guanlichu.org_name
            xdz_list = []
            for xiandizhan in xiandizhan_list:
                xdz_context = {"id":xiandizhan.id,"text": xiandizhan.org_name}
                xdz_list.append(xdz_context)
            glc_context = {"id":guanlichu.id, "text": guanlichu_name, "children": xdz_list}
            list_tmp.append(glc_context)
        fenju_context = {"id":fenju.id, "text": fenju_name, "children": list_tmp}
        zxj_context.append(fenju_context)

    print("^^^^^^^^^^^^^^^^^^^^^^^^")
    print(zxj_context)
    return zxj_context
