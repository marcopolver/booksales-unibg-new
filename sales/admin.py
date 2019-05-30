from django.contrib import admin
from sales.models import StudentProfile, Title, BookAd, ClusteringInfo
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(Title)
admin.site.register(BookAd)
admin.site.register(ClusteringInfo)