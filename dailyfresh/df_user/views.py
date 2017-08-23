from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from hashlib import sha1
from .models import *

def register(request):
    return render(request, 'df_user/register.html')

def register_handle(request):
    post = request.POST

    uname = post.get("user_name")
    upwd1 = post.get("pwd")
    upwd2 = post.get("cpwd")
    uemail = post.get("email")

# check whether the password entered for the twice time is consistent
    if upwd1 != upwd2:
        return redirect('/user/register')

# password encryption
    s1 = sha1()
    s1.update(upwd1.encode('utf-8'))
    upwd3 = s1.hexdigest()

    user_info = UserInfo()
    user_info.uname = uname
    user_info.upwd = upwd3
    user_info.uemail = uemail
    user_info.save()

    return redirect('/user/login')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname = uname).count()
#    return HttpResponse(count)
    return JsonResponse({'count':count})

def login(request):
    user_name = request.COOKIES.get('user')
    content = {'user': user_name}
    return render(request, 'df_user/login.html', content)

def user_info_handle(request):
    post = request.POST
    input_uname = post.get("username")
    input_pwd = post.get("pwd")

    s1 = sha1()
    s1.update(input_pwd.encode('utf-8'))
    upwd1 = s1.hexdigest()

    db_objects = UserInfo.objects.filter(uname=input_uname, upwd=upwd1)

#        response = rende_to_response("df_user/user_center_info.html")
#        response.set_cookie('user', 'input_uname')
#        return response
    if len(db_objects) == 0:
        return redirect('/user/login')
#TODO:js
    response = redirect("/user/info/")
    request.session['user_id'] = db_objects[0].id
    request.session['user_name'] = db_objects[0].uname

    if post.get("isRemeberUser") == 'checkbox':
        response.set_cookie('user', input_uname)

    return response

def user_center_info(request):
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')
    user_email = UserInfo.objects.get(id=user_id).uemail

    content = {
        'title':'用户中心',
        'user_name':user_name,
        'user_email':user_email
    }

    return render(request, 'df_user/user_center_info.html', content)

def user_order(request):
    return render(request, 'df_user/user_center_order.html')

def user_site(request):
    user = UserInfo.objects.get(id=request.session.get('user_id'))
    if request.method == 'POST':
        post = request.POST
        user.urecipients = post.get('recipients')
        user.udelivery_address = post.get('address')
        user.upostcode = post.get('postcode')
        user.uphone_number = post.get('phone')
        user.save()

    content = {"user":user}
    return render(request, 'df_user/user_center_site.html', content)