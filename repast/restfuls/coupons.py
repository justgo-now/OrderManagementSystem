# coding: utf8
from flask.ext import restful
from ..services.do_coupons import DoCoupons


class UpdateUserCoupons(restful.Resource):
    """ds"""
    @staticmethod
    def get(coupons_id):
        DoCoupons.update_coupons(coupons_id)
        DoCoupons.update_coupons_total(coupons_id)
        json = []
        json.append(['s'])
        return json