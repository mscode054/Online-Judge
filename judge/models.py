from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

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
    time_of_submission=models.DateTimeField('submitted at')
    

class TestCase(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    input=models.TextField()
    output=models.TextField()







