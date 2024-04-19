from django.contrib import admin
from authen.models import CustomUser, BlacklistedToken

admin.site.register(CustomUser)
admin.site.register(BlacklistedToken)
