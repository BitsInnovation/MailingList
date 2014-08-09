def create_confirmation_email(group):
  from list.models import Email
  confirmation_template = None
  try:
    confirmation_template = Email.objects.get(name="confirmation")
  except:
    confirmation_template = Email(name="confirmation",
                                  group = group,
                                  subject = "Confirm your subscription",
                                  body = """Hey {{subscriber.first_name}}!

                                  Please confirm your subscription to {{group.name}} list!

                                  Click here to confirm: https://mailinglist.herokuapp.com/confirm/{{gs.activation_key}}

                                  Thanks!

                                  -- Chris
                                  """,
                                  days=0)
    confirmation_template.save()
  print(confirmation_template)
  return confirmation_template

def queue_confirmation_email(user, group, activation_key):
  from list.models import EmailQueue
  # add email in email queue move to the top of the queue
  email = EmailQueue(subscriber=user, email=create_confirmation_email(group))
  email.save()
