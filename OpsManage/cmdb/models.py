# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


#
# class Employee(models.Model):
#     name = models.CharField(max_length=20)


# 资产总表信息
class Asset(models.Model):
    """   所有资产的共有数据表   """
    asset_type_choice = (
        (str(1), '服务器'),
        (str(2), '网络设备'),
        (str(3), '安全设备'),
        (str(4), '存储设备'),
        (str(5), '其他'),
    )

    asset_status = (
        (str(1), '使用中'),
        (str(2), '未使用'),
        (str(3), '故障'),
        (str(4), '其它'),
    )

    network_choice = (
        (str(1), '控制专网'),
        (str(2), '业务内网'),
        (str(3), '业务外网'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    asset_name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')  # 不可重复
    asset_no = models.CharField(max_length=50, unique=True, verbose_name='资产编号')  # 不可重复
    network_location = models.CharField(choices=network_choice, max_length=64, verbose_name='所属网络')
    organization = models.ForeignKey('Organization', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(choices=asset_status, max_length=50, default=0, verbose_name='设备状态')

    # vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.CASCADE)
    # model = models.CharField(max_length=128, null=True, blank=True, verbose_name='设备型号')
    model = models.ForeignKey('Device_model', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备型号')
    sn = models.CharField(max_length=128, unique=True, verbose_name='产品序列号')  # 不可重复

    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='admin')
    idc = models.ForeignKey('Idc', null=True, blank=True, on_delete=models.CASCADE)
    cabinet = models.ForeignKey('Cabinet', null=True, blank=True, on_delete=models.CASCADE)

    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, null=True, blank=True, verbose_name='来源合同')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, null=True, blank=True, verbose_name='供应厂商')
    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    c_time = models.DateField(null=True, blank=True, verbose_name='批准日期')
    m_time = models.DateField(auto_now=True, verbose_name='更新日期')
    memo = models.CharField(max_length=400, null=True, blank=True, verbose_name='备注')
    height=models.SmallIntegerField(blank=True, null=True, verbose_name='高度')
    cab_location = models.SmallIntegerField(blank=True, null=True, verbose_name='机柜位置')
    qrcode = models.URLField(max_length=200, null=True, blank=True, verbose_name='二维码')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.asset_name)

    class Meta:
        db_table = 'cmdb_asset'
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']


# 以下为资产商务信息

class Organization(models.Model):
    """ 组织机构  """
    parent_org = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='parent_level')
    org_name = models.CharField(max_length=64, unique=True, verbose_name='单位名称')
    org_address = models.CharField(max_length=64, blank=True, null=True, verbose_name='单位地址')
    org_memo = models.CharField(max_length=64, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.org_name

    class Meta:
        db_table = 'cmdb_organization'
        verbose_name = '所属单位'
        verbose_name_plural = verbose_name


class Contract(models.Model):
    """  合同  """
    contract_number = models.CharField(max_length=128, unique=True, verbose_name='合同编号号')
    contract_name = models.CharField(max_length=64, verbose_name='合同名称')
    contract_content = models.TextField(blank=True, null=True, verbose_name='合同内容')
    contract_memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.contract_name

    class Meta:
        db_table = 'cmdb_contract'
        verbose_name = '合同'
        verbose_name_plural = verbose_name


class Vendor(models.Model):
    """  生产厂商  """
    vendor_name = models.CharField(max_length=64, unique=True, verbose_name='厂商名称')
    vendor_phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='支持电话')
    vendor_memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.vendor_name

    class Meta:
        db_table = 'cmdb_vendor'
        verbose_name = '生产厂商'
        verbose_name_plural = verbose_name


class Supplier(models.Model):
    """   供应商  """
    supplier_name = models.CharField(max_length=64, unique=True, verbose_name='供应商名称')
    supplier_contacts = models.CharField(max_length=64, verbose_name='供应商联系人')
    supplier_phone = models.CharField(max_length=64, verbose_name='供应商电话')
    supplier_memo = models.CharField(max_length=64, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.supplier_name

    class Meta:
        db_table = 'cmdb_supplier'
        verbose_name = '供应商'
        verbose_name_plural = verbose_name


# 以下为机房机柜信息

class Idc(models.Model):
    """ 数据机房 """
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    idc_name = models.CharField(max_length=255, verbose_name="机房名称")
    idc_address = models.CharField(max_length=100, blank=True, verbose_name="机房地址")
    idc_memo = models.TextField(max_length=200, blank=True, verbose_name="备注信息")

    def __str__(self):
        return self.idc_name

    class Meta:
        db_table = 'cmdb_idc'
        verbose_name = '机房'
        verbose_name_plural = verbose_name


class Cabinet(models.Model):
    """ 机柜 """
    idc = models.ForeignKey('Idc', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所在机房')
    cabinet_name = models.CharField(max_length=100, verbose_name='机柜名称')
    cabinet_desc = models.CharField(max_length=100, blank=True, verbose_name='机柜描述')
    cabinet_height=models.SmallIntegerField(blank=True, null=True, verbose_name='机柜高度')

    def __str__(self):
        return self.cabinet_name

    class Meta:
        db_table = 'cmdb_cabinet'
        verbose_name = '机柜'
        verbose_name_plural = verbose_name


class CabinetSpace(models.Model):
    """ 机柜位置 """
    cabinet_space_choice = (
        (str(1), '1U'),
        (str(2), '2U'),
        (str(3), '3U'),
        (str(4), '4U'),
        (str(5), '5U'),
        (str(6), '6U'),
        (str(7), '7U'),
        (str(8), '8U'),
        (str(9), '9U'),
        (str(10), '10U'),
        (str(11), '11U'),
        (str(12), '12U'),
        (str(13), '13U'),
        (str(14), '14U'),
        (str(15), '15U'),
        (str(16), '16U'),
        (str(17), '17U'),
        (str(18), '18U'),
        (str(19), '19U'),
        (str(20), '20U'),
        (str(21), '21U'),
        (str(22), '22U'),
        (str(23), '23U'),
        (str(24), '24U'),
        (str(25), '25U'),
        (str(26), '26U'),
        (str(27), '27U'),
        (str(28), '28U'),
        (str(29), '29U'),
        (str(30), '30U'),
        (str(31), '31U'),
        (str(32), '32U'),
        (str(33), '33U'),
        (str(34), '34U'),
        (str(35), '35U'),
        (str(36), '36U'),
        (str(37), '37U'),
        (str(38), '38U'),
        (str(39), '39U'),
        (str(40), '40U'),
        (str(41), '41U'),
        (str(42), '42U'),
    )
    asset = models.ForeignKey('Asset',  blank=True, null=True, on_delete=models.SET_NULL, verbose_name='机柜空间')
    cabinet = models.ForeignKey('Cabinet', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所在机柜')
    cabinet_location = models.CharField(max_length=64, choices=cabinet_space_choice, blank=True, verbose_name='机柜位置')

    def __str__(self):
        return '资产：%s-- 机柜：%s--位置：%s ' % (self.asset, self.cabinet, str(self.cabinet_location))

    class Meta:
        db_table = 'cmdb_cabinetspace'
        unique_together = (('cabinet', 'cabinet_location'),)
        verbose_name = '机柜位置'
        verbose_name_plural = verbose_name
        ordering = ['cabinet', 'cabinet_location']


# 以下为资产分类信息

class Server(models.Model):
    """  服务器设备  """
    sub_asset_type_choice = (
        (str(1), 'PC服务器'),
        (str(2), '小型机'),
        (str(3), '刀片机'),
        (str(4), '虚拟机'),
        (str(5), '容器'),
    )

    os_type_choice = (
        (str(1), 'Windows'),
        (str(2), 'Unix'),
        (str(3), 'Linux'),
        (str(4), 'Other'),
    )

    created_by_choice = (
        (str(1), '自动添加'),
        (str(2), '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！
    sub_asset_type = models.CharField(choices=sub_asset_type_choice, max_length=64, default=0, verbose_name='服务器类型')
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name='添加方式')
    microcode = models.CharField(max_length=32, verbose_name='微码版本')
    hosted_on = models.ForeignKey('self', on_delete=models.CASCADE, related_name='hosted_on_server',
                                  blank=True, null=True)  # 虚拟机专用字段
    os_type = models.CharField(choices=os_type_choice, max_length=64, blank=True, null=True, verbose_name='操作系统类型')
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行版本')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='系统版本')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (
            self.asset.asset_name, self.get_sub_asset_type_display(), self.asset.model, self.asset.sn)

    class Meta:
        db_table = 'cmdb_server'
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
        ordering = ['sub_asset_type', 'asset']


class SecurityDevice(models.Model):
    """  安全设备  """
    sub_asset_type_choice = (
        (str(1), '防火墙'),
        (str(2), '入侵检测设备'),
        (str(3), '入侵防御设备'),
        (str(4), '综合安全网关'),
        (str(5), '数据库审计系统'),
        (str(6), '运维审计系统'),
        (str(7), '防病毒网关'),
        (str(8), 'WAF防火墙'),
        (str(9), '安全配置核查'),
        (str(10), '网络准入系统'),
        (str(11), '网闸设备'),
        (str(12), 'VPN设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')
    memo = models.TextField(max_length=200, blank=True, verbose_name="备注信息")

    def __str__(self):
        return self.asset.asset_name + '--' + self.get_sub_asset_type_display() + ' id:%s' % self.id

    class Meta:
        db_table = 'cmdb_securitydevice'
        verbose_name = '安全设备'
        verbose_name_plural = verbose_name
        ordering = ['sub_asset_type']


class StorageDevice(models.Model):
    """  存储设备  """
    sub_asset_type_choice = (
        (str(1), '磁盘阵列'),
        (str(2), '网络存储器'),
        (str(3), '光纤交换机'),
        (str(4), '磁带库'),
        (str(5), '磁带机'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='存储设备类型')

    def __str__(self):
        return self.asset.asset_name + '--' + self.get_sub_asset_type_display() + ' id:%s' % self.id

    class Meta:
        db_table = 'cmdb_storagedevice'
        verbose_name = '存储设备'
        verbose_name_plural = '存储设备'
        ordering = ['sub_asset_type']


class NetworkDevice(models.Model):
    """   网络设备 """
    sub_asset_type_choice = (
        (str(1), '路由器'),
        (str(2), '交换机'),
        (str(3), '工业交换机'),
        (str(4), '无线控制器'),
        (str(5), '无线AP'),
    )
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='网络设备类型')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (
            self.asset.asset_name, self.get_sub_asset_type_display(), self.asset.model, self.asset.sn)

    class Meta:
        db_table = 'cmdb_networkdevice'
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'
        ordering = ['sub_asset_type']


class Software(models.Model):
    """  只保存付费购买的软件   """
    sub_asset_type_choice = (
        (str(1), '操作系统'),
        (str(2), '数据库'),
        (str(3), '中间件'),
    )

    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='软件类型')
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField(max_length=64, unique=True, help_text='例如: CentOS release 6.7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        db_table = 'cmdb_software'
        verbose_name = '软件/系统'
        verbose_name_plural = '软件/系统'


# 以下为配件信息

class RAM(models.Model):
    """ 内存 """
    ram_status_choice = (
        (str(1), '正常'),
        (str(2), '故障'),
        (str(3), '下线'),
    )
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    ram_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存型号')
    ram_brand = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存品牌')
    ram_volume = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存容量')
    ram_slot = models.SmallIntegerField(blank=True, null=True, verbose_name='内存插槽')
    ram_status = models.CharField(choices=ram_status_choice, max_length=100, blank=True, null=True, verbose_name='内存状态')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.asset_name, self.ram_model, self.ram_slot, self.ram_volume)

    class Meta:
        db_table = 'cmdb_ram'
        unique_together = (('asset', 'ram_slot'),)
        verbose_name = '内存'
        verbose_name_plural = '内存'
        ordering = ['asset', 'ram_slot']


class CPU(models.Model):
    """ CPU """
    cpu_status_choice = (
        (str(1), '正常'),
        (str(2), '故障'),
        (str(3), '下线'),
    )
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='CPU型号')
    cpu_brand = models.CharField(max_length=100, blank=True, null=True, verbose_name='CPU生产商')
    cpu_speed = models.CharField(max_length=100, blank=True, null=True, verbose_name='CPU容量')
    cpu_core_count = models.SmallIntegerField(blank=True, null=True, verbose_name='CPU核数')
    cpu_slot = models.SmallIntegerField(blank=True, null=True, verbose_name='CPU插槽')
    cpu_status = models.CharField(choices=cpu_status_choice, max_length=100, blank=True, null=True,
                                  verbose_name='CPU状态')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.asset_name, self.cpu_model, self.cpu_slot, self.cpu_speed)

    class Meta:
        db_table = 'cmdb_cpu'
        unique_together = (('asset', 'cpu_slot'),)
        verbose_name = 'CPU'
        verbose_name_plural = verbose_name
        ordering = ['asset', 'cpu_slot']


class Disk(models.Model):
    """ 硬盘信息 """
    disk_status_choice = (
        (str(1), '正常'),
        (str(2), '故障'),
        (str(3), '下线'),
    )
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    disk_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='硬盘名称')
    disk_volume = models.CharField(max_length=64, blank=True, null=True, verbose_name='硬盘容量')
    disk_model = models.CharField(max_length=64, blank=True, null=True, verbose_name='硬盘型号')
    disk_brand = models.CharField(max_length=32, blank=True, null=True, verbose_name='硬盘生产商')
    disk_serial = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘序列号')
    disk_slot = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘插槽')
    disk_status = models.CharField(choices=disk_status_choice, max_length=100, blank=True, null=True,)
    disk_attr = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘属性')

    def __str__(self):
        return 'name:%s--- slot:%s--- brand:%s---model:%s' % (
            self.asset.asset_name, self.disk_slot, self.disk_brand, self.disk_model)

    class Meta:
        db_table = 'cmdb_disk'
        unique_together = (("asset", "disk_slot"),)
        verbose_name = '磁盘'
        verbose_name_plural = verbose_name
        ordering = ['asset', 'disk_slot']


class Port(models.Model):
    """ 接口信息 """
    port_type_choice = (
        (str(1), 'Ethernet'),
        (str(2), 'GigabitEthernet'),
        (str(3), 'TenGigabitEthernet'),
        (str(4), 'Pos'),
        (str(5), 'Serial'),
        (str(6), 'vlan'),
        (str(7), 'Tunnel'),
    )

    port_status_choice = (
        (str(1), 'UP'),
        (str(2), 'DOWN'),
        (str(3), 'AdminDown'),
    )

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    port_type = models.CharField(choices=port_type_choice, max_length=100, blank=True, null=True, verbose_name='接口类型')
    port_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='接口名称')
    port_slot = models.CharField(max_length=32, blank=True, null=True, verbose_name='网卡槽位')
    vlan = models.CharField(max_length=32, blank=True, null=True, verbose_name='接口vlan')
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='接口地址')
    sub_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='接口副地址')
    mask = models.SmallIntegerField(blank=True, null=True, verbose_name='子网掩码')
    bandwidth = models.CharField(max_length=30, null=True, verbose_name='接口带宽')
    status = models.CharField(choices=port_status_choice, max_length=100, blank=True, null=True, verbose_name='接口状态')

    def __str__(self):
        return '设备名称：%s--- 接口类型：%s---接口地址： %s---接口槽位%s---接口状态:%s' % (
            self.asset.asset_name, self.port_type, self.ip, self.port_slot, self.status)

    class Meta:
        db_table = 'cmdb_port'
        unique_together = (('asset', 'port_name'), ('asset', 'ip', 'sub_ip'),)
        verbose_name = '接口'
        verbose_name_plural = verbose_name
        ordering = ['asset', 'port_slot']


class Parts(models.Model):
    """ 接口信息 """
    parts_status_choice = (
        (str(1), '正常'),
        (str(2), '故障'),
        (str(3), '下线'),
    )
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    parts_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='部件类型')
    parts_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='部件名称')
    parts_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='部件型号')
    parts_sn = models.CharField(max_length=100, blank=True, null=True, verbose_name='部件序列号')
    parts_slot = models.CharField(max_length=64, blank=True, null=True, verbose_name='硬盘插槽')
    parts_status = models.CharField(choices=parts_status_choice, max_length=100, blank=True, null=True,
                                    verbose_name='部件状态')
    memo = models.TextField(max_length=1000, blank=True, null=True, verbose_name='部件描述')

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.asset_name, self.parts_name, self.parts_type, self.parts_sn)

    class Meta:
        db_table = 'cmdb_parts'
        unique_together = (("asset", "parts_sn"), ("asset", "parts_slot"))
        verbose_name = '部件'
        verbose_name_plural = verbose_name
        ordering = ['asset', 'parts_slot']


class EventLog(models.Model):
    """
    日志.在关联对象被删除的时候，不能一并删除，需保留日志。因此，on_delete=models.SET_NULL。
    """
    event_type_choice = (
        (str(1), '硬件变更'),
        (str(2), '新增配件'),
        (str(3), '设备下线'),
        (str(4), '设备上线'),
        (str(5), '定期维护'),
        (str(6), '业务上线'),
        (str(7), '其它'),
    )

    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    name = models.CharField(max_length=128, verbose_name='事件名称')
    event_type = models.CharField(max_length=64, choices=event_type_choice, default=4, verbose_name='事件类型')
    component = models.CharField(max_length=256, blank=True, null=True, verbose_name='事件子项')
    detail = models.TextField(verbose_name='事件详情')
    date = models.DateTimeField(auto_now_add=True, verbose_name='事件时间')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = '事件纪录'


class Device_model(models.Model):
    img = models.ImageField(upload_to='upload', height_field=None, width_field=None, blank=True, null=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='设备厂商')
    models = models.CharField(max_length=64, verbose_name='设备型号')



    def __str__(self):
        return self.models

    class Meta:
        verbose_name = '设备型号'
        verbose_name_plural = verbose_name
        unique_together = (("vendor", "models", "img"), )
