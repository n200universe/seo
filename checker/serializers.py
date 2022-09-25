from rest_framework import serializers

from .models import KeywordsChecker, Projects
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
# from datamanager.fields import ModelObjectidField, CurrentProjectDefault
import time


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'domain', 'frequency', 'notes', 'updated_recently', 'created_time')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordsChecker
        fields = ("history",)

    def __init__(self, model, *args, fields='__all__', **kwargs):
        self.Meta.model = model
        self.Meta.fields = fields
        super().__init__()

    class Meta:
        pass

class KeywordsCheckerSerializer(serializers.ModelSerializer):
    # average_position = serializers.SerializerMethodField()
    # def get_average_position(self, obj):
    #     return obj.average_position
  
    history = serializers.SerializerMethodField()
    def get_history(self, keywords):
        if hasattr(keywords, "history"):
            print("HAS ATTR")
            model = keywords.history.__dict__['model']
            fields = ['position' ,'updated']

            serializer = HistorySerializer(model, keywords.history.all().order_by('history_date'), fields=fields, many=True)
            serializer.is_valid()
            return serializer.data
        else: 
            print("NO ATTR")
            return
    class Meta:
        model = KeywordsChecker
        fields = ('id','keyword','change','position', 'url', 'title', 'meta_description', 'best', 'first', 'updated','history','project' )


# PERFORME BULK UPDATE USING LISTSERIALIZER
class CreateUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return [self.child.create(attrs) for attrs in validated_data]

    def update(self, instances, validated_data):
        instance_hash = {index: instance for index, instance in enumerate(instances)}

        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]

        return result
class BulkUpdateKeywordSerializers(serializers.ListSerializer):
    def create(self, validated_data):

        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        update_project_last_modified(result)

        return result

    def to_representation(self, instances):

        start = time.time()
        project = instances[0].project.pk
        rep_list = []
        for instance in instances:
            rep_list.append(
                dict(
                    id=instance.pk,
                    project=project,
                    description=instance.description,
                    name=instance.name,
                    last_modified=instance.last_modified,
                )
            )

        print("to_rep", time.time() - start)

        return rep_list

    def update(self, instances, validated_data):
        start = time.time()

        instance_hash = {index: instance for index, instance in enumerate(instances)}
        print("instance hash", time.time() - start)
        start = time.time()
        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]
        print("update instance", time.time() - start)
        start = time.time()

        print(self.child.Meta.read_only_fields)
        writable_fields = [
            x
            for x in self.child.Meta.fields
            if x not in self.child.Meta.read_only_fields + ("project",)
        ]
        # bulk update doesn't modify auto_now fields in django
        if "last_modified" in self.child.Meta.fields:
            writable_fields += ["last_modified"]
            last_modified = timezone.now()
            for instance in result:
                instance.last_modified = last_modified
        print("lst modified", time.time() - start)
        start = time.time()

        try:
            self.child.Meta.model.objects.bulk_update(result, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)

        print("bulk update", time.time() - start)
        start = time.time()

        update_project_last_modified(result)
        print("project lm", time.time() - start)
        start = time.time()

        return result
def update_project_last_modified(instances):

    if isinstance(instances, list):
        project = instances[0].project
        project.last_modified = timezone.now()
        project.save()