#!/usr/bin/env python
# encoding: utf-8


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^add_question/$', views.AddQuestionView.as_view(), name='add_question'),

    url(r'^question_list/$', views.QuestionListView.as_view(), name='question_list'),
  
    url(r'^questionSearch/$',views.QuestionSearchView.as_view(),name='question_Search'),
  
    url(r'^filterCategory/$',views.FlterCategoryView.as_view(),name='filterCategory'),

    url(r'^hot_spot/$', views.HotSpotView.as_view(), name='hot_spot'),

    url(r'^remove_question/', views.RemoveQuestionView.as_view(), name='remove_question'),

    url(r'^recommendQuestion/$', views.RecommendQuestionView.as_view(), name='recommend_question'),

]