from django.contrib import admin
from .models import *

class MouseAdmin(admin.ModelAdmin):
    pass
class BrandAdmin(admin.ModelAdmin):
    pass
class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Mouse, MouseAdmin)
admin.site.register(Brand, MouseAdmin)
admin.site.register(Category, MouseAdmin)

# Register your models here.
