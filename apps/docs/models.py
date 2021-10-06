from django.db import models
from django.db.models import CharField, Model
#from djangotoolbox.fields import ListField
#from django_mysql.models import ListCharField
#from django.contrib.postgres.fields import ArrayField
from django.conf import settings
#from .storages import MyLocalStorage, MyRemoteStorage
import json
from userinfo.models import User


# def select_storage():
#    return MyLocalStorage() if settings.DEBUG else MyRemoteStorage()

class Kategori(models.Model):
    name = models.CharField(null=False, max_length=400)
    sort = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)

    def serialize(self):
        try:
            return {
                "id": str(self.id),
                "name": self.name,
                "sort": str(self.sort),
                "parent": str(self.parent.id),
            }
        except:
            return {
                "id": str(self.id),
                "name": self.name,
                "sort": str(self.sort),
                "parent": '',
            }


class Document(models.Model):
    #kategori = models.CharField(max_length=500)  # ,verbose_name='Kategori'
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, blank=True, null=True, related_name='kategori_id')
    # likes = ArrayField(
    #         models.CharField(max_length=45, blank=True)
    #     )
    # views = ArrayField(
    #         models.CharField(max_length=45, blank=True)
    #     )
    likes = models.CharField(max_length=500, blank=True, null=True)
    likes_count = models.IntegerField(default=0)

    def set_likes(self, x):
        self.likes = json.dumps(x)

    def get_likes(self):
        return json.loads(self.likes)
    # likes = models.ListCharField(
    #     base_field=models.CharField(max_length=45),
    #     size=1000,
    #     max_length=(1000 * 11)  # 6 * 10 character nominals, plus commas
    # )
    #likes = ListField()
    views = models.CharField(max_length=500, blank=True, null=True)
    views_count = models.IntegerField(default=0)
    # def set_views(self, x):
    #    self.views = json.dumps(x)
    # def get_views(self):
    #    return json.loads(self.views)
    level = models.IntegerField(default=1)  # ,verbose_name="Level"
    create_date = models.DateTimeField(
        verbose_name='create_date', auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='update_date', auto_now_add=True)

    def serialize(self):
        return {
            "id": str(self.id),
            "kategori": self.kategori.serialize(),
            "likes": self.likes,
            "likes_count": str(self.likes_count),
            "views": self.views,
            "views_count": str(self.views_count),
            "level": str(self.level),
            "create_date": self.create_date,
            "update_date": self.update_date,
        }


class DetailDocument(models.Model):
    version = models.CharField(max_length=45, default='1')
    contents = models.TextField(blank=True, null=True)
    doc_file = models.CharField(max_length=500)
    title = models.CharField(max_length=500, blank=False, null=False, unique=True)
    pages = models.IntegerField(default=0)
    views = models.CharField(max_length=500, blank=True, null=True)
    views_count = models.IntegerField(default=0)
    likes = models.CharField(max_length=500, blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    document = models.ForeignKey(
        Document, on_delete=models.DO_NOTHING, related_name='documents')
    status = models.CharField(max_length=20, blank=True, null=True, default='active') 
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": str(self.id),
            "version": self.version,
            "contents": self.contents,
            "doc_file": self.doc_file,
            "pages": str(self.pages),
            "document": self.document.serialize(),
            "status": self.status,
            "create_date": self.create_date,
            "update_date": self.update_date,
        }

class Bab(models.Model):
    bab = models.CharField(max_length=500, verbose_name='Bab')
    sub_bab = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField()
    text1 = models.TextField(default='')
    page = models.CharField(max_length=45)
    endpage = models.CharField(max_length=45, default = '0')
    path = models.CharField(max_length=500, blank=True, null=True)
    likes = models.CharField(max_length=500, blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    detaildocument = models.ForeignKey(
        DetailDocument, on_delete=models.DO_NOTHING, related_name='detaildocument_id')
    create_date = models.DateTimeField(
        verbose_name='create_date', auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='update_date', auto_now_add=True)
    
class Babs(models.Model):
    # bab = models.CharField(max_length=500)
    # sub_bab = models.CharField(max_length=500, blank=True)
    text = models.TextField()
    text1 = models.TextField(default='')
    page = models.CharField(max_length=45)
    path = models.CharField(max_length=500, blank=True, null=True)
    detaildocument = models.ForeignKey(
        DetailDocument, on_delete=models.DO_NOTHING, related_name='detaildocument_ids')
    create_date = models.DateTimeField(
        verbose_name='create_date', auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='update_date', auto_now_add=True)


class Log(models.Model):
    action = models.CharField(max_length=45, verbose_name='Action')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    create_date = models.DateTimeField(
        verbose_name='create time', auto_now_add=True)
    #document = models.OneToOneField(DetailDocument, on_delete=models.DO_NOTHING)
    document = models.ForeignKey(DetailDocument, on_delete=models.DO_NOTHING)
