def send_email(emailqueue):
  from django.core.mail import send_mail
  from django.template import Context, Template

  body = Template(emailqueue.email.body)
  subject = Template(emailqueue.email.subject)
  group = emailqueue.email.group
  subscriber = emailqueue.subscriber
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
    emailqueue.sent = True
    emailqueue.save()
  except:
    from datetime import datetime, timedelta
    days = timedelta(days=emailqueue.email.days)
    emailqueue.send_date = datetime.now() + days
    emailqueue.save()


def create_confirmation_email(group):
  from list.models import Email
  confirmation_template = None
  try:
    confirmation_template = Email.objects.get(name="confirmation")
  except:
    confirmation_template = Email(name="confirmation",
                                  group = group,
                                  subject = "Confirm your subscription",
                                  body =
"""Hey {{subscriber.first_name}}!

Please confirm your subscription to {{group.name}} list!

Click here to confirm:
https://mailinglist.herokuapp.com/confirm/{{gs.activation_key}}

Thanks!

-- Chris
""",
                                  days=0)
    confirmation_template.save()
  return confirmation_template

def queue_confirmation_email(user, group, activation_key):
  from list.models import EmailQueue
  # add email in email queue move to the top of the queue
  email = EmailQueue(subscriber=user, email=create_confirmation_email(group))
  email.save()

  # send confirmation email
  send_email(email)
