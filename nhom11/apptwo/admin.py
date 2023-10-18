from django.contrib import admin

from apptwo.models import AccessRecord,Topic,Webpage





class WebpageAdmin(admin.ModelAdmin):
    search_fields=('name',)
    list_display=['topic','name','url']
    fields=['name','url']

# class AccessRecordAdmin(admin.ModelAdmin):
#     search_fields=('date',)

class TopicAdmin(admin.ModelAdmin):
    search_fields=('name',)

admin.site.register(Webpage,WebpageAdmin)
admin.site.register(AccessRecord)
admin.site.register(Topic,TopicAdmin)