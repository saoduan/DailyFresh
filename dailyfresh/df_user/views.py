from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
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
    if uname == None:
        return redirect
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
    user_name = request.COOKIES.get('user', '')

    content = {'user': user_name, 'error_name': 0, 'error_pwd': 0}
    return render(request, 'df_user/login.html', content)

def verifycode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 35

    im = Image.new('RGB', (width, height), bgcolor)

    draw = ImageDraw.Draw(im)

    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

#    font = ImageFont.truetype('FreeMono.ttf', 23)
    font = ImageFont.truetype('arial.ttf', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))

    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)

    del draw

    request.session['verifycode'] = rand_str

    import io
#    buf = io.StringIO()
    buf = io.BytesIO()

    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')

def user_info_handle(request):
    post = request.POST
    input_uname = post.get("username")
    input_pwd = post.get("pwd")
    is_remember = post.get("isRemeberUser", 0)

    db_objects = UserInfo.objects.filter(uname=input_uname)

#        response = rende_to_response("df_user/user_center_info.html")
#        response.set_cookie('user', 'input_uname')
#        return response
    if len(db_objects) == 1:
        s1 = sha1()
        s1.update(input_pwd.encode('utf-8'))
        upwd1 = s1.hexdigest()

        if db_objects[0].upwd == upwd1:
            response = HttpResponseRedirect('/user/info/')

            if is_remember == 'checkbox':
                response.set_cookie('user', input_uname)
            else:
                response.set_cookie('user', '', max_age=-1)

            request.session['user_id'] = db_objects[0].id
            request.session['user_name'] = db_objects[0].uname

            return response

        else:
            context = {'user':input_uname, 'error_name':0, 'error_pwd':1, 'pwd':input_pwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'user': input_uname, 'error_name':1, 'error_pwd': 0, 'pwd':input_pwd}
        return render(request, 'df_user/login.html', context)

#    response = redirect("/user/info/")
#    request.session['user_id'] = db_objects[0].id
#    request.session['user_name'] = db_objects[0].uname

#    if is_remember == 'checkbox':
#        response.set_cookie('user', input_uname)
#    else:
#        response.set_cookie('user', "", max_age=-1)
 #   return response


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
