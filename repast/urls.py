# coding: UTF-8
from flask.ext.admin import Admin
from flask.ext import restful

from . import app
from .weixin.verify import weixin
from .view.repasts import to_repast_by_stores_id
from .view.admin.group import GroupView
from .models.database import db
from .view.admin.index import HomeView
from .view.admin.brand import BrandView
from restfuls.return_group import GetGroup
from .view.home import *
from .view.myMsg import *
from .view.restaurant import *
from restfuls.return_group import *
from restfuls.store_search import *
from .view.admin.stores import StoresView
from .view.admin.queue_setting import QueueSettingView
from .view.admin.admin_login import *
from .view.admin.shop_assistant import ShopAssistantView
from .view.repasts import *
from .view.order_dishes.a_la_carte import ToOrderDishes,dish_selected
from .view.admin.dish import *
from .view.admin.package import PackageView
from .view.admin.dish_sort import DishSortView
from restfuls.queue import AjaxCallNumber
from services.food_list_service import GetDishes
from .view.order_dishes.my_coupons import *
from .restfuls.coupons import *
from .restfuls.dish import AddDish, ShowDish
from .view.order_dishes.static import *
from .view.order_dishes.a_la_carte import to_pay_1,to_pay_5


# 用户管理路径
# app.add_url_rule('url','method_name', method_name, method=('GET','POST'))
app.add_url_rule('/weixin', 'weixin', weixin, methods=('GET','POST'))
app.add_url_rule('/repast/<int:stores_id>', 'repast', to_repast_by_stores_id, methods=('GET','POST'))
# app.add_url_rule('/home','home',home,methods=('GET','POST'))
app.add_url_rule('/myMsg/','myMsg',myMsg,methods=('GET','POST'))
app.add_url_rule('/restaurant/','toRestaurant',toRestaurant,methods=('GET','POST'))
app.add_url_rule('/login/', 'login_view', login_view, methods=('GET', 'POST'))
app.add_url_rule('/register/','login_register', register_view, methods=('GET','POST'))
app.add_url_rule('/call_number/<int:shop_assistant_id>','to_call_number', to_call_number, methods=('GET','POST'))
app.add_url_rule('/do_call_number/<int:queue_id>','do_call_number', do_call_number, methods=('GET','POST'))
app.add_url_rule('/home/','to_home', to_home, methods=('GET','POST'))
app.add_url_rule('/home_page/','to_home_page', to_home_page, methods=('GET','POST'))
app.add_url_rule('/shop_assistant_login/','to_login', to_login, methods=('GET','POST'))
app.add_url_rule('/do_assistant_login/', 'do_assistant_login', do_assistant_login, methods=('GET','POST'))
app.add_url_rule('/order_dishes/','to_order_dishes', to_order_dishes, methods=('GET','POST'))
# 排队
app.add_url_rule('/q/my_queue/<int:user_id>', 'to_my_queue', to_my_queue, methods=('GET','POST'))
app.add_url_rule('/q/queue/<int:stores_id>', 'to_queue', to_queue, methods=('GET','POST'))
app.add_url_rule('/q/do_queue/','do_queue', do_queue, methods=('GET','POST'))
app.add_url_rule('/q/search/','to_search', to_search, methods=('GET','POST'))
app.add_url_rule('/q/search_result/', 'to_search_result', to_search_result, methods=('GET','POST'))
app.add_url_rule('/text/', view_func=ToOrderDishes.as_view('text'))
app.add_url_rule('/q/to_search_position/', 'to_search_position',to_search_position,methods=('GET','POST'))
app.add_url_rule('/to_reservation/', 'to_reservation', to_reservation, methods= ('GET', 'POST'))
app.add_url_rule('/q/do_cancel_queue/<int:queue_id>', 'do_cancel_queue', do_cancel_queue, methods= ('GET', 'POST'))
# 我的
app.add_url_rule('/m/my_page/', 'to_my_page', to_my_page, methods=('GET','POST'))
app.add_url_rule('/m/my_coupons/', 'deal_coupons', deal_coupons, methods=('GET', 'POST'))
app.add_url_rule('/m/my_line_up', 'to_my_line_up', to_my_line_up, methods=('GET', 'POST'))
app.add_url_rule('/location', 'to_location', location, methods=('GET', 'POST'))
app.add_url_rule('/m/mytel', 'to_mytel', myTel, methods=('GET', 'POST'))
app.add_url_rule('/m/my', 'to_my', my, methods=('GET', 'POST'))
# 点餐
app.add_url_rule('/f/meal_restaurant', 'to_meal_restaurant', to_meal_restaurant_list, methods=('GET', 'POST'))
app.add_url_rule('/f/package', 'to_package', to_package_list, methods=('GET', 'POST'))
app.add_url_rule('/f/meal_list', 'to_meal_list', to_meal_list, methods=('GET', 'POST'))
app.add_url_rule('/f/meal_search_position', 'to_meal_search_position', to_meal_search_position, methods=('GET', 'POST'))
# 优惠
app.add_url_rule('/y/on_sale','on_sale',on_sale,methods=('GET', 'POST'))
#支付

app.add_url_rule('/toPay', 'to_pay_1', to_pay_1, methods=('GET', 'POST'))
app.add_url_rule('/toPay5', 'to_pay_5', to_pay_5, methods=('GET', 'POST'))
#首页
app.add_url_rule('/introduce','to_introduce',to_introduce,methods=('GET','POST'))
app.add_url_rule('/food','to_food',to_food,methods=('GET','POST'))
#游戏
app.add_url_rule('/to_game','to_game', to_game,methods=('GET', 'POST'))
app.add_url_rule('/f/to_dish_selected', 'dish_selected', dish_selected, methods=('GET','POST'))
# 接口定义
api = restful.Api(app)
api.add_resource(GetGroup, '/restful/group')
api.add_resource(GetBrand, '/restful/brand/<int:group_id>')
api.add_resource(GetProvince, '/restful/province')
api.add_resource(GetCity, '/restful/city/<int:province_id>')
api.add_resource(GetCountry, '/restful/country/<int:city_id>')
api.add_resource(GetStores, '/restful/stores/<int:brand_id>')
api.add_resource(SearchStore,'/restful/searchStore')
api.add_resource(PositionStore,'/restful/positionStore')
api.add_resource(PositionStoreXY,'/restful/positionStoreXY')
api.add_resource(GetDishSort, '/restful/dish_sort/<int:brand_id>')
api.add_resource(GetPackage, '/restful/package/<int:brand_id>')
api.add_resource(GetDishSortDish, '/restful/sort/<int:package_id>')

api.add_resource(AjaxCallNumber, '/restful/call_number/<int:shop_assistant_id>')
api.add_resource(GetDishes,'/services/get_foods/<int:dish_sort_id>')
api.add_resource(UpdateUserCoupons,'/restful/coupons_id/<int:coupons_id>')
api.add_resource(AddDish, '/restful/add/dish')

# 获得已选菜品
api.add_resource(ShowDish, '/restful/get/choose/dish')


# 后台管理路径
admin = Admin(name=u'Home', index_view=HomeView())
admin.init_app(app)

admin.add_view(GroupView(db, name=u'集团', endpoint='group', category=u'管理'))
admin.add_view(BrandView(db, name=u'品牌', endpoint='brand', category=u'管理'))
admin.add_view(StoresView(db, name=u'餐厅', endpoint='stores', category=u'管理'))
admin.add_view(QueueSettingView(db, name=u'桌型维护', endpoint='queue'))
admin.add_view(ShopAssistantView(db, name=u'店员维护', endpoint='shop_assistant'))
admin.add_view(DishView(db, name=u'菜品', endpoint='dish', category=u'点菜'))
admin.add_view(PackageView(db, name=u'套餐', endpoint='package', category=u'点菜'))
admin.add_view(DishSortView(db, name=u'菜单分类', endpoint='dish_sort', category=u'点菜'))
