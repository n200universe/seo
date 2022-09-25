from tkinter.tix import Tree
from turtle import position
from django.db import models
from simple_history.models import HistoricalRecords
from django.db.models import Avg, Max, Min, Sum
class Projects(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=400)
    frequency = models.IntegerField(default=24)
    notes = models.TextField(null=True, blank=True)
    project_url = models.SlugField(blank=True)
    updated_recently = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_time']


class KeywordsChecker(models.Model):

    project = models.ForeignKey(Projects, on_delete=models.DO_NOTHING, null=True)
    keyword = models.CharField(max_length=1000)
    change = models.IntegerField(blank=True, null=True)
    position =models.IntegerField(blank=True, null=True)
    best=models.IntegerField(blank=True, null=True)
    first=models.IntegerField(blank=True, null=True)
    volume =models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    tags = models.TextField(null=True, blank=True)
    project_url = models.SlugField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.keyword

    # @property
    # def average_position(self):
    #     return self.position.Avg('position')['position_avg']


    class Meta:
        ordering = ['-updated']
