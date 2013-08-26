####################################################################
#                      Summarizer Configurations                   #
####################################################################
import os


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError, e:
        print 'Got keyError -reason "%s"' str(e)

USERNAME = get_env_variable('USERNAME')
PASSWORD = get_env_variable('PASSWORD')
SENDGRID_AUTH = get_env_variable('SENDGRID_AUTH')
ORGANIZATION = get_env_variable('ORGANIZATION')

# mailing configurations
SENDER = get_env_variable('SENDER')
SUBJECT = get_env_variable('SUBJECT')

RECEIVER = get_env_variable('RECEIVER')
RECEIVER_NAME = get_env_variable('RECEIVER_NAME')

USERS = {'ramana@agiliq.com': {'full_name': 'Venkata Ramana C',
                               'login': 'arjunc77'},

         'dheeru@agiliq.com': {'full_name': 'Dheeraj Kumar Ketireddy',
                               'login': 'dheeru0198'},

         'akshar@agiliq.com': {'full_name': 'Akshar Raaj',
                               'login': 'akshar-raaj'},

         'balu@agiliq.com': {'full_name': 'Bala Subrahmanyam Varanasi',
                             'login': 'Balu-Varanasi'},

         'shabda@agiliq.com': {'full_name': 'Shabda Raaj',
                               'login': 'shabda'},

         'bhaskar@agiliq.com': {'full_name': 'Bhaskar Rao',
                                'login': 'bhaskar'},

         'rakesh@agiliq.com': {'full_name': 'Rakesh Vidya Chandra',
                               'login': 'krvc'},

         'shiva@agiliq.com': {'full_name': 'Shiva Krishna',
                              'login': 'shivakrshn49'},

         'imohammed23@gmail.com': {'full_name': 'Imran Mohammed',
                                   'login': 'mipreamble'},

         'tuxcanfly@gmail.com': {'full_name': 'Jakh Daven',
                                 'login': 'tuxcanfly'}}


####################################################################
