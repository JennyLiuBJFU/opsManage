# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.article_index, name='wiki'),
    url(r'^view/(?P<pid>[0-9]+)/$', views.article_show, name='wiki_article_show'),
    url(r'^add/$', views.article_add, name='wiki_article_add'),
    url(r'^edit/(?P<pid>[0-9]+)/$', views.article_edit, name='wiki_article_edit'),
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^category/(?P<pid>[0-9]+)/$', views.article_category, name='wiki_category'),
    url(r'^tag/(?P<pid>[0-9]+)/$', views.article_tag, name='wiki_tag'),
    url(r'^archive/(?P<month>([0-9]{4})/([0-9]{2}))/$', views.article_archive, name='wiki_archive'),
    # url(r'^upload/(?P<path>(\S)*)', serve, {'document_root': MEDIA_ROOT + 'wiki/'}),
]
