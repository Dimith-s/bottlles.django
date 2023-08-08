# import os
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# from dotenv import load_dotenv

# load_dotenv()

# print(1)
# print(os.getenv('TWILIO_VERIFY_SERVICE_SID'))
# print(os.environ['TWILIO_VERIFY_SERVICE_SID'])
# print(2)
# client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
# verify = client.verify.services("VA588e18a00c7c5437a028d99a789e88cb")


# def send(phone):
#     print(verify)
#     verify.verifications.create(to=phone, channel='sms')


# def check(phone, code):
#     try:
#         result = verify.verification_checks.create(to=phone, code=code)
#     except TwilioRestException:
#         print('no')
#         return False
#     return result.status == 'approved'












import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    print(verify)
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'