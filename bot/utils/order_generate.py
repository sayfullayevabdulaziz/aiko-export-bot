import random
import string
import time

def generate_order_id():
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp}-{random_chars}"
