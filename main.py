from modules.bot import Bot
from modules.functionals.sending_messages import send_mail

import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

send_mail("doburghgh@gmail.com", "Test Mail", "This is a test :3")