# coding: utf-8
from sqlalchemy import Column, String, Integer
from database import Base
from base_class import InitUpdate

PACKAGE = 'package'

class Package(Base, InitUpdate):
    __tablename__ = PACKAGE
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    group_id = Column(Integer, nullable=False)
    group = Column(String(50), nullable=False)
    brand_id = Column(Integer, nullable=False)
    brand = Column(String(50), nullable=False)
    dish_sort_id = Column(String(20), nullable=False)
    dish_sort = Column(String(200), nullable=False)
    suitable_number = Column(Integer, nullable=False, server_default='0')

    def __init__(self, **kwargs):
        args = ('name', 'group_id','group','brand_id','brand','dish_sort_id','dish_sort', 'suitable_number')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('name', 'group_id','group','brand_id','brand','dish_sort_id','dish_sort', 'suitable_number')
        self.update_value(args, kwargs)
    @staticmethod
    def get_package_by_brand(brand_id):
        '''根据品牌获取套餐'''
        temp = [] # 临时集合， 方便view层调用
        package_count = Package.query.filter(Package.brand_id == brand_id).count()
        if package_count > 1:
            package = Package.query.filter(Package.brand_id == brand_id).all()
            for p in package:
                temp.append(p)
        else:
            package = Package.query.filter(Package.brand_id == brand_id).first()
            if package:
                temp.append(package)
        return temp

    @staticmethod
    def get_package_by_id(package_id):
        package = Package.query.filter(Package.id == package_id).first()
        return package