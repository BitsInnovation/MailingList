def send_email(email, subject, subscriber, group):
  from django.core.mail import send_mail
  from django.template import Context, Template

  body = Template(email)
  subject = Template(subject)
  gs = subscriber.groupsubscriber_set.get(group=group)
  data = {
    "subscriber": subscriber,
    "group": group,
    "gs": gs
  }

  body = body.render(Context(data))
  subject = subject.render(Context(data))

  try:
    send_mail(subject, body, "%s <%s>" % (group.from_name, group.from_email), [subscriber.email], fail_silently=False)
  except:
    pass


def create_confirmation_email(group):
  email = """
Hey {{subscriber.first_name}}!

Please confirm your subscription to %s list!

Click here to confirm:
https://mailinglist.herokuapp.com/confirm/{{gs.activation_key}}

Thanks!

-- Chris
""" % (group.name)
  subject = "Please confirm your subscription!"
  return (email, subject)

def queue_confirmation_email(user, group, activation_key):
  # add email in email queue move to the top of the queue
  email, subject = create_confirmation_email(group)
  send_email(email, subject, user, group)
