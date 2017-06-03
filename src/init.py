import telebot
import toml
import os

# get conf file:
telebot_config = os.getenv("TELEBOT_CONFIG")

if telebot_config:
    config = toml.loads(telebot_config)
else:
    telebot_conf_file = os.getenv("TELEBOT_CONFIG_FILE")
    if not telebot_conf_file:
        telebot_conf_file = "~/.telebot"

    telebot_conf_file = os.path.expanduser(telebot_conf_file)
    with open(telebot_conf_file) as conf:
        config = toml.loads(conf.read())

# DEBUG mode enabler
if 'logging' in config:
    log_level = config['logging']['debuglevel']
    levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
    if log_level in levels:
        telebot.logger.setLevel(log_level)
    else:
        telebot.logger.setLevel('NOTSET')


# init telebot
tb = telebot.TeleBot(config['security']['token'])


class TelebotObject():
    """global object"""

    def __init__(self, config):
        super(TelebotObject, self).__init__()

        if "IsAuthorised" in config['security']:
            self.IsAuthorised = config['security']['IsAuthorised']
            if type(self.IsAuthorised) != bool:
                self.panic()
        else:
            self.IsAuthorised = False

        if "secretQuestion" in config['security']:
            self.secretQuestion = config['security']['secretQuestion']
        else:
            self.secretQuestion = 'pass'

        if "insecFunc" in config['security']:
            self.InsecureFuncs = config['security']["insecFunc"]
        else:
            self.InsecureFuncs = ['sudo']

        if "whitelisted_users_id" in config['users']:
            self.whitelisted_users_id = config['users']["whitelisted_users_id"]

        # default working tree
        if "workDir" in config['properties']:
            self.workDir = config['properties']['workDir']
        else:
            self.workDir = os.path.expanduser("~/repos/")

    def panic(self):
        print("errors in configs")


# init global object
print(config)
tb_mem = TelebotObject(config)


#
