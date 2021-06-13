from django.contrib import admin
from app_users.models import UserProfileInfo,Query,AboutUs,Logo,Contact
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Query)
admin.site.register(AboutUs)
admin.site.register(Logo)
admin.site.register(Contact)
