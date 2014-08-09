from django.contrib import admin
from list.models import Subscriber, Group, Email, EmailQueue, GroupSubscriber

class GroupAdmin(admin.ModelAdmin):
  list_display = ('name', 'from_name', 'from_email')

class SubscriberAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'email')

class EmailAdmin(admin.ModelAdmin):
  list_display = ('name', 'group', 'subject', 'body', 'days')

class EmailQueueAdmin(admin.ModelAdmin):
  pass

class GroupSubscriberAdmin(admin.ModelAdmin):
  list_display = ('subscriber', 'group', 'confirmed')

admin.site.register(Group, GroupAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(EmailQueue, EmailQueueAdmin)
admin.site.register(GroupSubscriber, GroupSubscriberAdmin)
