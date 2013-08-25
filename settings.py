####################################################################
#                      Summarizer Configurations                   #
####################################################################
import os


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError, e:
        print 'Got keyError -reason "%s"' str(e)

username = get_env_variable('username')
password = get_env_variable('username')
sendgrid_auth = get_env_variable('sendgrid_auth')
ORGANIZATION = get_env_variable('ORGANIZATION')

# mailing configurations
SENDER = get_env_variable('SENDER')
SUBJECT = get_env_variable('SUBJECT')

####################################################################
