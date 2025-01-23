from modules.bot import Bot

import string
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

Bot.check_tags(
    'Hallo, ich hätte gern ein Test1, oder Test2, vielen dank im vorraus :)')
