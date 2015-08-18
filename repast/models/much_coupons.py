# coding: UTF-8
from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME


MUCHCOUPONS='muchcoupons'

class MuchCoupons(Base,InitUpdate):
    '''优惠券'''
    __tablename__ = MUCHCOUPONS
    id = Column(Integer, primary_key=True)
    package_id=Column(Integer,nullable=False)
    description = Column(String(200), nullable=True)
    dish_name = Column(String(100), nullable=False)
    sale=Column(Integer,nullable=False)
    begin_time = Column(DATETIME, nullable=False)
    end_time = Column(DATETIME, nullable=False)

    def __init__(self, **kwargs):
        args = ('package_id','description','dish_name','sale','begin_time','end_time')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('package_id','description','dish_name','sale','begin_time','end_time')
        self.init_value(args, kwargs)

    @staticmethod
    def get_coupons_by_id(coupons_id):
        coupons = MuchCoupons.query.filter(MuchCoupons.id == coupons_id).first()
        return coupons