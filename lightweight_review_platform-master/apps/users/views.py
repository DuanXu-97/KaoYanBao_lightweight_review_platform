from django.shortcuts import render
from .models import UserProfile, EmailVerifyRecord, UserWeaknessCategory, UserWeaknessTag
from django.views.generic import View
from .forms import RegisterForm, LoginForm, ActiveForm, UserCenterForm, ChangePasswordForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from main_platform.models import CommonWeaknessCategory, CommonWeaknessTag
from django.contrib import auth
import os,base64, time, datetime
# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html',
                      context={'register_form': register_form,})

    def post(self, request):
    
        register_form = RegisterForm(request.POST)
        user_email=request.POST.get('email', '')
        is_email_exist=UserProfile.objects.filter(email=user_email)

        if is_email_exist:
            return HttpResponse('{"status": "fail", "msg": "邮箱已注册，请更换邮箱注册"}',content_type='application/json')
        elif register_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password1', '')
            e_mail = request.POST.get('email', '')

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.password = make_password(pass_word)
            user_profile.email = e_mail
            user_profile.is_active = False

            user_profile.save()

            send_register_email(e_mail, 'register')


            return HttpResponse('{"status": "success", "url":"/"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "注册失败，请重新注册"}', content_type='application/json')


class ActiveUserView(View):
    """
    激活用户
    """
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        all_weakness_category = CommonWeaknessCategory.objects.all()
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                login(request, user)
                # 激活成功跳转到登录页面
                return render(request, 'actScsAndIntTags.html',
                              context={'courseList': all_weakness_category})
        else:
            return render(request, 'register.html', {"msg": "您的激活链接无效", "active_form": active_form})

    def post(self, request):
        length = int(request.POST.get('length', '1'))
        for i in range(0, length):
            course_id = request.POST.get('userInitialTags[{}][course_id]'.format(str(i)), '')
            initialTag = request.POST.get('userInitialTags[{}][initialTags]'.format(str(i)), '')
            initialTag_list = str(initialTag).split("_")[1:]
            course_id = int(course_id)
            cwc = CommonWeaknessCategory.objects.get(id=course_id)
            course_name = cwc.name
            uwc = UserWeaknessCategory.objects.create(name=course_name, user_belong_id=request.user.id)
            uwc.save()
            for i in range(0, len(initialTag_list)):
                uwt = UserWeaknessTag.objects.create(name=initialTag_list[i], category_belong_id=uwc.id)
                uwt.save()
        return HttpResponse('{"status": "success"}', content_type='application/json')

class InitialTags_againView(View):                 #推题页面如果没有注册时为填写标签，则在此处会追加标签
    def post(self,request):
        length = int(request.POST.get('length', '1'))
        for i in range(0, length):
            course_id = request.POST.get('userInitialTags[{}][course_id]'.format(str(i)), '')
            initialTag = request.POST.get('userInitialTags[{}][initialTags]'.format(str(i)), '')
            initialTag_list = str(initialTag).split("_")[1:]
            if course_id!='' and initialTag !='':
                course_id = int(course_id)
                cwc = CommonWeaknessCategory.objects.get(id=course_id)
                course_name = cwc.name
                uwc = UserWeaknessCategory.objects.get(name=course_name, user_belong_id=request.user.id)
                for i in range(0, len(initialTag_list)):
                    uwt = UserWeaknessTag.objects.create(name=initialTag_list[i], category_belong_id=uwc.id)
                    uwt.save()
            else:
                pass
        return HttpResponse('{"status": "success"}', content_type='application/json')
      
      

class UserLogoutView(View):
    """
    用户注销
    """
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect("/")


class UserLoginView(View):
    """
    登录
    """

    def get(self, request):
        rediect_url = request.GET.get('next', '')
        return render(request, 'index.html',
                      {'redirect_url', rediect_url})

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponse('{"status": "success", "url": "/"}', content_type='application/json')
                else:
                    return HttpResponse('{"status": "fail", "msg": "用户未激活, 请先激活用户"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "用户或密码错误!"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "用户或密码格式不正确!"}', content_type='application/json')


class UserCenterView(View):
    """
    用户中心
    """

    def get(self, request):
        usercenter_form = UserCenterForm()
        return render(request, 'userCenter.html',)

    def post(self, request):
        usercenter_form= UserCenterForm(request.POST)
            #django获取页面中登录的用户
        if usercenter_form.is_valid():
            user_nickname=request.POST.get('nickname', '')
            user_gender=request.POST.get('gender','')
            user_birthday=request.POST.get('birthday','')
            user_presentCollege=request.POST.get('presentCollege','')
            user_targetCollege=request.POST.get('targetCollege','')
            user_motto=request.POST.get('motto','')
            request.user.nickname=user_nickname
            request.user.gender=user_gender
            request.user.birthday=user_birthday
            request.user.presentCollege=user_presentCollege
            request.user.targetCollege=user_targetCollege
            request.user.motto=user_motto
            request.user.save()
            return HttpResponse('{"status": "success", "url":"/"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "信息保存失败"}', content_type='application/json')


class UploadImageView(View):
    """
    用户修改图像
    """

    def get(self,request):
        return render(request, 'userCenter.html', {'request.user.avatar': request.user.avatar})


    def post(self,request):
        data_img=request.POST.get('img','')     #获取前端传来数据
        result = data_img.split(',')[1]          #字符串分割获取图片的base64编码
        imgdata = base64.b64decode(result)        #将base64编码解码转换为二进制数据
        user_dir = 'static/img/'+request.user.username
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        store_addr = user_dir+'/' + 'avatar' +'.jpg'  #设定图片保存地址，根据用户名来对图片进行命名
        file = open(store_addr, 'wb')
        file.write(imgdata)
        file.close()                             #根据二进制数据转换为图片
        avatar = 'img/'+request.user.username+'/' + 'avatar' + '.jpg'
        user = UserProfile.objects.get(email=request.user.email)
        user.avatar = avatar
        user.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class PasswordChangeView(View):
    """
    密码修改
    """
    def get(self, request):
        return render(request, 'userCenter.html')

    def post(self, request):

        changepassword_form = ChangePasswordForm(request.POST)
        if changepassword_form.is_valid():
            previousPassword = request.POST.get('previousPassword', '')
            newPassword1 = request.POST.get('newPassword1', '')
            newPassword2 = request.POST.get('newPassword2', '')
            if newPassword1 != newPassword2:
                return HttpResponse('{"status": "fail", "msg": "两次密码不一致"}', content_type='application/json')
            user =UserProfile.objects.get(username=request.user.username)
            if user:
                user.password = make_password(newPassword1)
                user.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "修改密码失败，用户不存在"}', content_type='application/json')
        return HttpResponse('{"status": "fail", "msg": "修改密码失败, 请重新尝试"}', content_type='application/json')


class CheckinView(View):
    """
    签到打卡
    """
    def post(self, request):
        checkinDate = request.POST.get('checkinDate', datetime.datetime.now().strftime("%Y-%m-%d"))
        if checkinDate != '':
            checkinDate = datetime.datetime.strptime(checkinDate, "%Y-%m-%d").date()
        else:
            return HttpResponse('{"status": "fail", "msg": "无法读取当前日期" }', content_type='application/json')
        lastCheckinDate = request.user.lastCheckinDate
        if lastCheckinDate == None:
            lastCheckinDate = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        if checkinDate > lastCheckinDate:
            user = UserProfile.objects.get(id=request.user.id)
            user.lastCheckinDate = checkinDate
            user.checkin_days += 1
            user.save()
            return HttpResponse('{"status": "success", "msg": "打卡成功，再接再厉" }', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "你已经打过卡了，请明天再来噢" }', content_type='application/json')


class MemoView(View):
    """
    备忘录
    """

    def post(self, request):
        print(request)
        memoContent = request.POST.get('memoContent', '')
        user = UserProfile.objects.get(id=request.user.id)
        user.memo = memoContent
        user.save()
        return HttpResponse('{"status": "success"}', content_type='application/json')


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            if user.check_password(password):
                return user
        except Exception as e:
            return None


          






