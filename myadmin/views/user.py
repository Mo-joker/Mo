import random
from string import hexdigits
from xml.etree.ElementTree import PI
from django.shortcuts import render
from myadmin.models import User
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime


def index(request, pIndex=1):
    '''浏览用户信息'''
    # 获取用户列表ulist
    ob = User.objects
    ulist1 = ob.filter(status__lt=9)  # 隐藏已删除的员工

    # 获取搜索条件
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        ulist1 = ulist1.filter(Q(username__contains=kw)
                               | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)

    # 执行分页
    pIndex = int(pIndex)
    page = Paginator(ulist1, 5)  # 每页显示5条数据
    maxpages = page.num_pages  # 总页数
    plist = page.page_range
    if pIndex < 1:
        pIndex = 1
    if pIndex > maxpages:
        pIndex = maxpages
    ulist2 = page.page(pIndex)

    context = {"userlists": ulist2, "plist": plist,
               "pIndex": pIndex, "mywhere": mywhere}
    return render(request, 'myadmin/user/index.html', context)


def add(request):
    '''进入添加用户信息表单'''
    return render(request, 'myadmin/user/add.html')


def insert(request):
    '''新增用户信息'''
    ob = User()
    # 获取前端输入的用户信息
    try:
        username = request.POST['username']
        nickname = request.POST['nickname']
        pwd = request.POST['password']
        pwd2 = request.POST['repassword']
    except:
        context = {"info": "获取用户信息出错"}
        return render(request, 'myadmin/info.html', context)

    # 判断密码是否一致
    if pwd != pwd2:
        context = {"info": "两次输入的密码不一致，请检查密码"}
        return render(request, 'myadmin/info.html', context)
 
    # hash存储用户密码
    import hashlib
    pwd = hashlib.md5()
    salt = random.randint(100000, 999999)
    psw_str = str(request.POST.get('inputpsw'))+str(salt)
    pwd.update(psw_str.encode('utf-8'))
    ob.username = username
    ob.nickname = nickname
    ob.password_hash = pwd.hexdigest()
    ob.password_salt = salt
    ob.status = 1
    ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()

    context = {"info": "员工添加成功！"}
    return render(request, 'myadmin/info.html', context)


def delete(request,uid):
    '''删除用户信息'''
    try:
        ob =User.objects.get(id=uid)
        print('del user : ' ,ob)
        ob.status = 9
        ob.save()
        context = {"info": "员工删除成功！"}
    except Exception as err:
        context = {"info": "员工删除失败！"}
    return render(request, 'myadmin/info.html', context)


def edit(request,uid):
    '''进入编辑用户信息表单'''
    user = User.objects.get(id=uid)
    print('user info ',user)

    context = {"user": user}
    return render(request, 'myadmin/user/edit.html', context)



def update(request,uid):
    '''执行用户信息修改'''
    user = User.objects.get(id=uid)
    user.username = request.POST['username']
    user.nickname = request.POST['nickname']
    user.status = request.POST['status']
    user.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.save()
    context = {"info":"用户信息更新成功"}
    return render(request, 'myadmin/info.html', context)