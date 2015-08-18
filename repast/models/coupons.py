# coding: UTF-8
from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, Integer, String, ForeignKey, DATE


COUPONS='coupons'

class Coupons(Base,InitUpdate):
    '''优惠券'''
    __tablename__ = COUPONS
    id = Column(Integer, primary_key=True)
    stores_id=Column(Integer,nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    dish_name = Column(String(100), nullable=False)
    present=Column(String(100), nullable=True)
    price = Column(Integer, nullable=False)
    cou_price = Column(Integer, nullable=False)
    begin_time = Column(DATE, nullable=False)
    end_time = Column(DATE, nullable=False)
    total = Column(Integer,nullable=True)

    def __init__(self, **kwargs):
        args = ('name','description','dish_name','present','price','cou_price','begin_time','end_time','total')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('name','description','dish_name','present','price','cou_price','begin_time','end_time','total')
        self.init_value(args, kwargs)

    @staticmethod
    def get_coupons_by_id(coupons_id):
        coupons = Coupons.query.filter(Coupons.id == coupons_id).first()
        return coupons

    @staticmethod
    def get_all_coupons():
        all_coupons= Coupons.query.all()[:5]
        return all_coupons