#from rest_framework_mongoengine.serializers import DocumentSerializer, DynamicDocumentSerializer
#from rest_framework_mongoengine.serializers import serializers
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .models import Document, DetailDocument, Bab, Log, Kategori
import functools


# class DocCreateSerializer(serializers.Serializer):
class DocCreateSerializer(serializers.ModelSerializer):  # serializers.Serializer
    #kategori = serializers.CharField(max_length=45)
    #level = serializers.IntegerField()
    documents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Document
        fields = '__all__'
        depth = 0

    def create(self, validated_data):
        return Document.objects.create(**validated_data)


class DetailDocCreateSerializer(serializers.ModelSerializer):
    #documents = serializers.RelatedField(source='document', read_only=True)
    #documents = serializers.RelatedField(many=True, read_only='True')
    # PrimaryKeyRelatedField
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all(),
                                                  many=False)
    #document = serializers.PrimaryKeyRelatedField(many=False)

    class Meta:
        model = DetailDocument
        #fields = '__all__'
        #depth = 0
        fields = ('id', 'version', 'contents', 'doc_file', 'title',
                  'pages', 'create_date', 'update_date', 'document')

    def create(self, validated_data):
        return DetailDocument.objects.create(**validated_data)
    # def validate(self, attrs):
    #     doc = attrs['doc_file']
    #     fs = FileSystemStorage(
    #         location=f'{settings.MEDIA_ROOT}/documents/',
    #         base_url=f'{settings.MEDIA_URL}/documents/'
    #     )
    #     if doc.content_type != 'application/pdf':
    #         raise ValidationError('File type not PDF')
    #     filename = fs.save(doc.name, doc)
    #     file_path = fs.url(filename)
    #     attrs['doc'] = file_path
    #     return attrs


class DocSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'


class DocDetailSerializer(serializers.ModelSerializer):
    # total_likes = serializers.IntegerField()

    class Meta:
        model = DetailDocument
        fields = '__all__'


class DocTotalDetailSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField()

    class Meta:
        model = DetailDocument
        fields = '__all__'

class DocTotalDetailSerializerNoAnnotate(serializers.ModelSerializer):
    # total_likes = serializers.IntegerField()

    class Meta:
        model = DetailDocument
        fields = '__all__'


class BabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bab
        fields = ["id", "bab", "sub_bab", "page", "endpage", "path"]


class DocSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'kategori']


class DocDetailSearchSerializer(serializers.ModelSerializer):
    document = DocSearchSerializer(read_only=True)

    class Meta:
        model = DetailDocument
        fields = ['id', 'title', 'pages', 'document', "create_date"]


class BabSearchSerializer(serializers.ModelSerializer):
    detaildocument = DocDetailSearchSerializer(read_only=True)

    class Meta:
        model = Bab
        fields = ['id', 'bab', 'sub_bab', 'page',
                  'text', 'text1', 'path', 'detaildocument']
        depth = 2


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ["document", "create_date"]


class KategoriCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

    def create(self, validated_data):
        return Kategori.objects.create(**validated_data)
