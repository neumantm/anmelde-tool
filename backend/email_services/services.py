from backend import settings
from .choices import EmailType
from .threads.registration import EmailThreadRegistration
from .threads.payment_reminder import EmailThreadPaymentReminder

url = getattr(settings, 'FRONT_URL', '')
email_active = getattr(settings, 'SEND_MAIL', False)


def send_registration_created_mail(**kwargs):
    instance_id = kwargs.get('instance_id')
    if instance_id and email_active:
        EmailThreadRegistration(instance_id, EmailType.RegistrationCreated).start()


def send_payment_reminder_mail(event_id):
    EmailThreadPaymentReminder(event_id, EmailType.PaymentReminder).start()
