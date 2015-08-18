#encoding:utf8

from repast.models.coupons import Coupons
from ..util.session_common import get_session_user
from ..services.user_service import UserService
from repast.models.database import db

class DoCoupons():
    @staticmethod
    def do_coupons(stores_id):
        coupons_name = Coupons.query.filter(Coupons.stores_id == stores_id).all()
        return coupons_name

    @staticmethod
    def get_coupons_by_id(coupons_id):
        coupons = Coupons.query.filter(Coupons.id == coupons_id).first()
        return coupons


    @staticmethod
    def update_coupons(coupons_id):
        user_id = get_session_user()
        user_service=UserService()
        user_service.update_user_coupons(user_id,coupons_id)

    @staticmethod
    def get_coupons():
        user_id = get_session_user()
        user_service = UserService()
        user = user_service.get_user_by_id(user_id)
        temp = []
        coupons_array = []
        if user:
            try:
                temp = user.coupons_id.split(',')
            except:
                pass
        if temp:
            for t in temp:
                coupons = DoCoupons.get_coupons_by_id(t)
                coupons_array.append(coupons)

        return coupons_array

    @staticmethod
    def update_coupons_total(coupons_id):
        coupons= Coupons.get_coupons_by_id(coupons_id)
        if coupons.total >0:
            coupons.total = coupons.total-1
            db.commit()