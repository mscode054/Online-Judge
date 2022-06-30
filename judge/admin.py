from django.contrib import admin
from .models import Problem,User,Solution,TestCase

# Register your models here.
admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(TestCase)