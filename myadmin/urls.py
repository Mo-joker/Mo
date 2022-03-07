from email.policy import default
from django.urls import path
from myadmin.views import index,user

urlpatterns = [
    path('', index.index,name='myadmin_index'),

     # 后台管理员路由
    path('login', index.login, name="myadmin_login"),
    path('dologin', index.dologin, name="myadmin_dologin"),
    path('logout', index.logout, name="myadmin_logout"),
    path('verify', index.verify, name="myadmin_verify"), #验证码

    # 员工路由
    path('user', user.index,name='myadmin_user_index'),
    path('user/<int:pIndex>', user.index,name='myadmin_user_index'),
    path('user/add', user.add, name='myadmin_user_add'),
    path('user/insert', user.insert, name='myadmin_user_insert'),
    path('user/del/<int:uid>', user.delete, name='myadmin_user_delete'),
    path('user/edit/<int:uid>', user.edit, name='myadmin_user_edit'),
    path('user/update/<int:uid>', user.update, name='myadmin_user_update'),

]
