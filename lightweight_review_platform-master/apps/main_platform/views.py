from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import View
from .models import Question, Tag, Hotspot, CommonWeaknessCategory, CommonWeaknessTag
from users.models import UserWeaknessTag,UserWeaknessCategory,Search,UserProfile
from .forms import QuestionForm
from pure_pagination import PageNotAnInteger, Paginator
import json
from django.conf import settings
import datetime,os,math
from django.db.models import Q
from .Apriori import *

# Create your views here.

class IndexView(View):
    """
    首页
    """
    def get(self, request):
        return render(request, 'index.html',)


class QuestionListView(View):
    """
    难题列表
    """

    def get(self, request):
        all_question = Question.objects.filter(user_belong_id=request.user.id).order_by("-created_time")
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_question, 5, request=request)
        all_question = p.page(page)

        return render(request, "question_list.html",
                  context={"question_list": all_question,})


class AddQuestionView(View):
    """
    难题添加
    """

    def post(self, request):
        question_tags = request.POST.get('tags', '')
        tags_list = str(question_tags).split("_")[1:]
        question_form = QuestionForm(request.POST)
        question_form.instance.user_belong_id = request.user.id
        if question_form.is_valid():
            question_form.save()
            question = Question.objects.get(id=question_form.instance.id)
            for question_tag in tags_list:
                tags = question.tags
                tags.create(name=question_tag)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class RemoveQuestionView(View):
    """
    删除难题
    """
    def get(self, request):
        ret = {'status': 'success'}
        try:
            question_id = request.GET.get('id')
            question = Question.objects.get(id=question_id)
            question_tag = question.tags.all()
            for tag in question_tag:
                tag.delete()
            question.delete()
        except Exception as e:
            ret['status'] = 'fail'
        return HttpResponse(json.dumps(ret), content_type='application/json')
      
      
class QuestionSearchView(View):
    """
    搜索功能函数
    """
    def post(self,request):
        key_words=request.POST.get('search')
        if Search.objects.filter(user_belong_id=request.user.id):
            Search.objects.filter(user_belong_id=request.user.id).update(search_content=key_words)
        else:
            user_search = Search.objects.create(user_belong_id=request.user.id,search_content=key_words)
            user_search.save()
        question_list=Question.objects.filter(Q(user_belong_id=request.user.id, title__icontains=key_words) | Q(user_belong_id=request.user.id, answer__icontains=key_words) | Q(user_belong_id=request.user.id, note__icontains=key_words))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(question_list, 5, request=request)
        question_list = p.page(page)
        return render(request, "question_list.html",context={'searchContent':key_words,'question_list':question_list})

    def get(self,request):
        key_words=Search.objects.get(user_belong_id=request.user.id)
        questionlist = Question.objects.filter(Q(user_belong_id=request.user.id, title__icontains=key_words) | Q(user_belong_id=request.user.id, answer__icontains=key_words) | Q(user_belong_id=request.user.id, note__icontains=key_words))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(questionlist, 5, request=request)
        questionlist = p.page(page)
        return render(request, "question_list.html",context={'searchContent':key_words,'question_list':questionlist})
      
class FlterCategoryView(View):
    """
    按照学科分类
    """
    def get(self,request):
        Category=request.GET.get('filterCategory')
        question_list=Question.objects.filter(user_belong_id=request.user.id,category=Category)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(question_list, 5, request=request)
        question_list = p.page(page)
        return render(request,"question_list.html",context={'filterCategory':Category,'question_list':question_list,})



class WangEditor_uploadView(View):
    """
    富文本编辑器图片上传
    """
    def post(self,request):
        files = request.FILES.get('images')  # 得到文件对象
        today = datetime.datetime.today()

        file_dir = settings.MEDIA_ROOT + '/%d/%d/%d/' % (today.year, today.month, today.day)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + files.name
        open(file_path, 'wb+').write(files.read())  # 上传文件
        upload_info = {"errno":0, "data":[settings.MEDIA_URL +'%d/%d/%d/' % (today.year, today.month, today.day)+ files.name]}
        upload_info = json.dumps(upload_info)   #wangeditor返回值json格式比较特殊，需要按照上面配置
        return HttpResponse(upload_info, content_type="application/json")



class HotSpotView(View):
    """
    时事广场
    """

    def get(self, request):
        all_hotspot = Hotspot.objects.all().order_by("-date")

        return render(request, 'hotspot.html',
                      context={'hotspot_list': all_hotspot})


class Thumbs_UpView(View):
    """
    对于题库中题目点赞
    """
    def post(self,request):
        rq_id=request.POST.get('rqid')
        tag_id=request.POST.get('tagid')
        rquestion=Question.objects.get(user_belong_id=2,id=rq_id)
        rtag=rquestion.tags.get(id=tag_id)
        rtag.score+=1
        rtag.save()
        info={"status":"success","msg":"点赞成功"}
        info = json.dumps(info)
        return HttpResponse(info,content_type="application/json")

class cancel_thumbsUpView(View):
    """
    对题目中标签取消点赞
    """
    def post(self,request):
        rq_id=request.POST.get('rqid')
        tag_id=request.POST.get('tagid')
        rquestion=Question.objects.get(user_belong_id=2,id=rq_id)
        rtag=rquestion.tags.get(id=tag_id)
        rtag.score-=1
        rtag.save()
        info={"status":"success","msg":"取消点赞成功"}
        info = json.dumps(info)
        return HttpResponse(info,content_type="application/json")


class Thumbs_DownView(View):
    """
    对于题库中题目点踩
    """
    def post(self,request):
        rq_id=request.POST.get('rqid')
        tag_id=request.POST.get('tagid')
        rquestion=Question.objects.get(user_belong_id=2,id=rq_id)
        rtag=rquestion.tags.get(id=tag_id)
        rtag.score-=1
        rtag.save()
        info={"status":"success","msg":"点踩成功"}
        info = json.dumps(info)
        return HttpResponse(info,content_type="application/json")

class cancel_thumbsDownView(View):
    """
    对题目中标签取消点踩
    """
    def post(self,request):
        rq_id=request.POST.get('rqid')
        tag_id=request.POST.get('tagid')
        rquestion=Question.objects.get(user_belong_id=2,id=rq_id)
        rtag=rquestion.tags.get(id=tag_id)
        rtag.score+=1
        rtag.save()
        info={"status":"success","msg":"取消点踩成功"}
        info = json.dumps(info)
        return HttpResponse(info,content_type="application/json")

class AddTagtoQuesView(View):
    """
    添加问题标签
    """
    def post(self,request):
        rq_id = request.POST.get('rqid')
        tag = request.POST.get('tag')
        rquestion=Question.objects.get(id=rq_id)
        add_tag=rquestion.tags.create(name=tag,score=1)
        add_tag.save()
        info={"status":"success","msg":"添加标签成功"}
        info = json.dumps(info)
        return HttpResponse(info,content_type="application/json")

class RemoveTagtoQuesView(View):
    """
    用户删除自己添加的标签
    """
    def post(self,request):
        rq_id = request.POST.get('rqid')
        tag = request.POST.get('tag')
        rquestion = Question.objects.get(id=rq_id)
        rquestion.tags.get(name=tag).delete()
        info = {"status": "success", "msg": "添加标签成功"}
        info = json.dumps(info)
        return HttpResponse(info, content_type="application/json")


def sim_cos(weekness_user,weekness_ques):        #采用计算余弦相似度的相似度计算算法
    sim={}
    for item in weekness_user:
        if item in weekness_ques:
            sim[item]=1
    if len(sim)==0:
        return 0
    pSum=sum([weekness_user[item]*weekness_ques[item] for item in sim])
    sum1Sq=sum([pow(weekness_user[item],2) for item in weekness_user])
    sum2Sq = sum([pow(weekness_ques[item], 2) for item in weekness_ques])
    mul=math.sqrt(sum1Sq*sum2Sq)
    if mul==0:
        return 0
    simility=float(pSum)/mul
    return simility

class RecommendQuestionView(View):
    """
    大头戏，智能推题
    """
    def get(self, request):
        if request.user.is_authenticated():

            ## 题库推荐的处理
            rqLibList=Question.objects.filter(user_belong_id=2)      #得到属于管理员的题目，即属于题库中的题目
            length=len(rqLibList)
            subject="计算机网络"
            UWC=UserWeaknessCategory.objects.get(user_belong_id=request.user.id,name=subject) #取用户的弱项分类
            all_weekness_category=CommonWeaknessCategory.objects.all()
            UWT=UserWeaknessTag.objects.filter(category_belong_id=UWC.id)  #取用户该弱项分类的标签
            if not UWT.exists():
                return render(request, 'addInitialTags.html',context={'courseList':all_weekness_category})
            else:
                length_UWT=len(UWT)                                              #取该用户的弱项分类标签的长度
                weekness_user={}
                threshold_u_q=0.3                                                      #阈值的设置
                rqLibList_result=[]
                for k in range(0,length_UWT):
                    weekness_user[UWT[k].name]=UWT[k].score  #创建一个用户的弱项标签字典
                for i in range(0,length):
                    rqtaglist=rqLibList[i].tags.all()      #取出该题目所有的标签，构成一个列表对象
                    length_taglist=len(rqtaglist)
                    weekness_ques={}
                    for j in range(0,length_taglist):     #得到一个标签的字典
                        weekness_ques[rqtaglist[j].name]=rqtaglist[j].score
                    simility_u_q=sim_cos(weekness_user,weekness_ques)
                    if (simility_u_q>threshold_u_q):
                        rqLibList_result.append(rqLibList[i])
            ####用户推荐的处理
            user_all=UserProfile.objects.filter(~Q(id=request.user.id)&~Q(id=2)) #得到除自己本身和管理员之外的用户对象
            user_length=len(user_all)
            threshold_u_u=0.5           #用户推荐时的阈值设置
            rqShareList_result=[]
            for i in range(0,user_length):
                weekness_user1={}
                UWC1=UserWeaknessCategory.objects.get(user_belong_id=user_all[i].id,name=subject) #取用户的弱项分类
                UWT1 = UserWeaknessTag.objects.filter(category_belong_id=UWC1.id)  # 取用户该弱项分类的标签
                length_UWT1 = len(UWT1)
                for k in range(0,length_UWT1):
                    weekness_user1[UWT1[k].name]=UWT1[k].score               #创建一个用户的弱项标签字典
                simility_u_u = sim_cos(weekness_user, weekness_user1)        #计算两个用户的相似度
                if simility_u_u>=threshold_u_u:
                    rqShareList=Question.objects.filter(user_belong_id=user_all[i].id)
                    rqShareList_result.extend(rqShareList)
               
            #关联推荐的处理
            subject = "计算机网络"             # 先挖掘关联规则
            database_subject_id = UserWeaknessCategory.objects.filter(name=subject).values_list('id',flat=True)   #得到了数据库中所有用户计算机网络学科的薄弱项分类的id
            dataset = []
            for id in database_subject_id:
                term = UserWeaknessTag.objects.filter(category_belong_id=id).values_list('name',flat=True)  # term为弱项的集合
                dataset.append(term)  # 将其以列表的形式插入到dataset的末尾
            result_direct = main(dataset)                 # 关联规则的挖掘来自Apriori的main函数,返回规则字典
            #UWT为该用户的弱项查询集合
            uwt_list=UWT.values_list('name',flat=True)    #只取用户的弱项的名称
            uwt_set=set(uwt_list)
            result_lenth=len(result_direct)
            result_direct_key=list(result_direct.keys())       #返回key
            result_direct_value=list(result_direct.values())   #返回values
            question_all=Question.objects.filter(category='major')   #.values_list('id',flat=True) #获取所有专业课的题目id
            question_length=len(question_all)
            rqRelationList=[ ]
            for i in range(0,result_lenth):
                if result_direct_key[i].issubset(uwt_set):      #若弱项集合是用户弱项的子集，即用户含有该弱项集合
                    for j in range(0,question_length):
                        this_ques_tagall=set(question_all[j].tags.all().values_list('name',flat=True))  #直接转换为set类型
                        if len(this_ques_tagall&result_direct_value[i])>0:
                            rqRelationList.append(question_all[j])
            rqRelationList_result=[]
            for rq in rqRelationList:                          #关联推荐的题目去重
                if rq not in rqRelationList_result:
                    rqRelationList_result.append(rq)
            return render(request, 'recommendQuestion.html',context={'rqLibList':rqLibList_result,'rqShareList':rqShareList_result,'rqRelationList':rqRelationList_result})
        else:
            return render(request, 'recommendQuestion.html')
