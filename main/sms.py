import random

# here we generate our verification code and send it via our sms client
# as it optional to add sms  utils, i just created verification code function


def send_verification_code(phone_number):
    verification_code = random.randint(100000, 999999)
    message = f"Your verification code is {verification_code}"
    print(f"Sending to {phone_number}: {message}")
    return verification_code
