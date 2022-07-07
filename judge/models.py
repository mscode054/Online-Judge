from django.db import models
import os
# Create your models here.

class Problem(models.Model):
    title=models.CharField(max_length=100)
    statement=models.TextField()
    difficulty_level=models.CharField(max_length=20)
    code=models.TextField(blank=True)
    def __str__(self):
        return self.title

class Solution(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    verdict=models.CharField(max_length=100)
    def get_upload_path_inp(instance, filename):
        return os.path.join("uploads/sol/problem_%d" % instance.problem.id,filename)
    submitted_code=models.FileField(upload_to=get_upload_path_inp)
    time_of_submission=models.DateTimeField('submitted at')
    

class TestCase(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    def get_upload_path_inp(instance, filename):
        return os.path.join("uploads/input/problem_%d" % instance.problem.id,filename)

    def get_upload_path_out(instance, filename):
        return os.path.join("uploads/output/problem_%d" % instance.problem.id,filename)
    
    input=models.FileField(upload_to=get_upload_path_inp)
    output=models.FileField(upload_to=get_upload_path_out)







