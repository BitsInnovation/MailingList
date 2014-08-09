from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from list.models import Subscriber, GroupSubscriber

# confirms email for 1 mailing list
def confirm_email(request, activation_key):
  try:
    gs = GroupSubscriber.objects.get(activation_key=activation_key)
    gs.confirmed = True
    gs.save()
  except:
    raise Http404

  return redirect("http://www.chrisbartos.com")

# unsubscribes from 1 mailinglist
def unsubscribe(request, activation_key):

  gs = GroupSubscriber.objects.get(activation_key=activation_key)
  gs.delete()

  return redirect("http://www.chrisbartos.com")
