# Generated by Django 2.1.1 on 2018-09-07 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='分类名称')),
            ],
            options={
                'verbose_name': 'wiki分类',
                'verbose_name_plural': 'wiki分类',
                'db_table': 'opsmanage_wiki_category',
                'permissions': (('can_read_wiki_category', '读取分类权限'), ('can_change_wiki_category', '更改分类权限'), ('can_add_wiki_category', '添加分类权限'), ('can_delete_wiki_category', '删除分类权限')),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='评论用户')),
                ('email', models.EmailField(max_length=255, verbose_name='邮箱')),
                ('url', models.URLField(blank=True, verbose_name='文章地址')),
                ('text', models.TextField(verbose_name='文章类容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
            ],
            options={
                'verbose_name': 'wiki文章评论',
                'verbose_name_plural': 'wiki文章评论',
                'db_table': 'opsmanage_wiki_comment',
                'permissions': (('can_read_wiki_comment', '读取评论权限'), ('can_change_wiki_comment', '更改评论权限'), ('can_add_wiki_comment', '添加评论权限'), ('can_delete_wiki_comment', '删除评论权限')),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, unique=True, verbose_name='标题')),
                ('content', models.TextField(verbose_name='类容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.Category', verbose_name='分类')),
            ],
            options={
                'verbose_name': 'wiki文章',
                'verbose_name_plural': 'wiki文章',
                'db_table': 'opsmanage_wiki_post',
                'permissions': (('can_read_wiki_post', '读取文章权限'), ('can_change_wiki_post', '更改文章权限'), ('can_add_wiki_post', '添加文章权限'), ('can_delete_wiki_post', '删除文章权限')),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='标签类型')),
            ],
            options={
                'verbose_name': 'wiki标签',
                'verbose_name_plural': 'wiki标签',
                'db_table': 'opsmanage_wiki_tag',
                'permissions': (('can_read_wiki_tag', '读取标签权限'), ('can_change_wiki_tag', '更改标签权限'), ('can_add_wiki_tag', '添加标签权限'), ('can_delete_wiki_tag', '删除标签权限')),
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='wiki.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.Post', verbose_name='文章id'),
        ),
    ]
