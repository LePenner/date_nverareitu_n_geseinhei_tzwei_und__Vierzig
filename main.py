from modules.bot import Bot
from modules.functionals.sending_messages import send_mail

import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

send_mail('thilo.butt@gmail.com', 'Test Header',
          'Jetzt wird wieder in die Hände gespuckt, wir steigern das Bruttosozialprodukt!')
