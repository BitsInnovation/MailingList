from django.db import models
from list.utils import queue_confirmation_email
import hashlib
import random

def create_activation_key(user):
  salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
  activation_key = hashlib.sha224(salt+user.email+user.first_name).hexdigest()
  return activation_key[:40]

class Group(models.Model):
  name = models.CharField(max_length=255, unique=True, blank=False)
  from_name = models.CharField(max_length=30, default="Chris Bartos", blank=False)
  from_email = models.EmailField(blank=False, default="me@chrisbartos.com")
  signup_form = models.TextField(default="", blank=True)

  def __unicode__(self):
    return u'%s' % (self.name)

  def save(self, *args, **kwargs):
    self.signup_form ="""<form action="https://mailinglist.herokuapp.com/subscribe/%s" method="post">
  <label for="first_name">First name:</label>
  <input type="text" name="first_name" />
  <label for="email">Email:</label>
  <input type="email" name="email" />
  <input type="submit" />
</form>
""" % (self.name)
    super(Group, self).save(*args, **kwargs)

class Subscriber(models.Model):
  first_name = models.CharField(max_length=30, blank=False)
  email = models.EmailField(blank=False)
  group = models.ManyToManyField(Group, through="GroupSubscriber")
  subscribe_date = models.DateField(auto_now_add=True)

  def __unicode__(self):
    return u'%s (%s)' % (self.first_name, self.email)

class GroupSubscriber(models.Model):
  group = models.ForeignKey(Group)
  subscriber = models.ForeignKey(Subscriber)
  confirmed = models.BooleanField(default=False)
  activation_key = models.CharField(max_length=40, default="", blank=True)

  def save(self, *args, **kwargs):
    send_confirmation = False
    if not self.id:
      send_confirmation = True
    self.activation_key = create_activation_key(self.subscriber)
    super(GroupSubscriber, self).save(*args, **kwargs)
    if send_confirmation == True:
      queue_confirmation_email(self.subscriber, self.group, self.activation_key)


# Email for each correspondence
#
# Group - specifies the group that should receive this email.
# Subject - specifies the subject of the email message
# Body - specifies the body of the email that our subscribers will receive
# Days - specifies how many days AFTER subscription begins or AFTER email was
#        created that the users will receive this email. When an email
#        is created, everybody who is already in the system will have an
#        email in the email_queue. Anybody who subscribes after will
#        receive all the emails in a queue at a specified date.
class Email(models.Model):
  name = models.CharField(max_length=40, blank=False, default="")
  group = models.ForeignKey(Group)
  subject = models.CharField(max_length=255)
  body = models.TextField()
  days = models.IntegerField(default=0)

  def save(self, *args, **kwargs):
    if not self.id:
      super(Email, self).save(*args, **kwargs)
      from datetime import date
      from list.models import EmailQueue, GroupSubscriber
      subscribers = GroupSubscriber.objects.filter(group=self.group, confirmed=True)
      for s in subscribers:
        emailQueue = EmailQueue(subscriber=s.subscriber, email=self, sent=False, send_date=date.today())
        emailQueue.save()
    else:
      super(Email, self).save(*args, **kwargs)

  def __unicode__(self):
    return u'%s : %s : %s' % (self.name, self.group.name, self.subject)

class EmailQueue(models.Model):
  subscriber = models.ForeignKey(Subscriber)
  email = models.ForeignKey(Email)
  sent = models.BooleanField(default=False)
  send_date = models.DateField()

  def __unicode__(self):
    return u'%s - %s : Sent(%s)' % (str(self.subscriber), self.email.subject, str(self.sent))

  def save(self, *args, **kwargs):
    if not self.id:
      from datetime import datetime, timedelta
      days = timedelta(days=self.email.days)
      self.send_date = datetime.now() + days
    super(EmailQueue, self).save(*args, **kwargs)
