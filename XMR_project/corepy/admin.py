from django.contrib import admin
from corepy import models
# Register your models here.

tables = [
    models.Industry,
    models.Site,
    models.SiteInfo,
    models.Readings,
    models.UserProfile,
    models.River,
    models.ExceedanceReports,
    models.Parameters

]

for table in tables:
    admin.site.register(table)