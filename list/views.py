from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from list.models import Subscriber, GroupSubscriber, Group

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

# subscribes someone to 1 mailinglist
def subscribe(request, group_name):
  if request.method == 'GET':
    raise Http404
  elif request.method == 'POST':
    group = Group.objects.get(name=group_name)
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    subscriber = None
    try:
      # subscriber might already exist
      subscriber = Subscriber.objects.get(email=email)
    except:
      # nope, create it
      subscriber = Subscriber(email=email, first_name=first_name)
      subscriber.save()
    gs = None
    try:
      # GroupSubscriber already exists?
      gs = GroupSubscriber.objects.get(group=group, subscriber=subscriber)
    except:
      # Nope, create it.
      gs = GroupSubscriber(group=group, subscriber=subscriber)
      gs.save()
  return redirect("http://www.chrisbartos.com")
