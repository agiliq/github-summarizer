import sendgrid

from auth import github_auth, sendgrid_auth
from datetime import datetime, timedelta
from dateutil import tz

from pygithub3 import Github
from pygithub3.services.repos import Commits


gh = Github(login=github_auth[0], password=github_auth[1])

####################################################################
#                      Summarizer Configurations                   #
####################################################################

organization = 'agiliq'

# mailing configurations
sender = "rakesh@agiliq.com"
subject = "Agiliq-Github Summary for the day "

####################################################################


def get_repos(organization):
    """
    Retuns all the repos in the given Organization
    """
    repos = gh.repos.list(organization).all()
    return repos


def get_user_objects(members):
    """
    Takes Github TeamMember objects and returns a list of
    Github User Objects.
    """
    users = []
    for member in members:
        users.append(gh.users.get(member.login))
    return users


def get_user_info(users):
    """
    Takes Github User objects and returns a list of tuples as below.
    [('rakesh@agiliq.com', 'Rakesh Vidya Chandra', 'krvc'),
     ('balu@agiliq.com', 'Bala Subrahmanyam Varanasi', 'Balu-Varanasi'),
    ]
    """
    user_info = []
    for user in users:
        try:
            email = user.email
        except AttributeError:
            email = ''
        item = email, user.name, user.login
        user_info.append(item)
    return user_info


def get_commits_list(repo):
    """
    Takes a repo and returns the commit list in 'master' branch
    """
    commits_list = []
    commits_list = Commits(user=organization,
                           repo=repo.name).list(sha='master',
                                                path=None).all()
    return commits_list


today = datetime.now()
today = today.replace(tzinfo=tz.tzlocal())
subject += today.strftime("%b %d %Y")

members = gh.orgs.members.list(organization).all()
users = get_user_objects(members)
email_to = get_user_info(users)


def send_mail(user_activity):
    """
    Takes user activity and sends email to all the members
    of the 'organization'
    """
    sendgrid_obj = sendgrid.Sendgrid(sendgrid_auth[0],
                                     sendgrid_auth[1],
                                     secure=True)

    html = "<html><body>"
    for key, value in user_activity.iteritems():
        if value:
            html += "<div>" + "<h3>" + key + "</h3>" + value + "</div>"
    html += "</body></html>"

    message = sendgrid.Message(sender,
                               subject,
                               "",
                               "<div>" + html + "</div>")
    for person in email_to:
        message.add_to(person[0], person[1])

    sendgrid_obj.smtp.send(message)


def main():

    this_day = (today - timedelta(hours=24)).date()

    github_body = ""
    user_activity = {}

    organization_repos = get_repos()

    for repo in organization_repos:
        commit_list = get_commits_list(repo)

        for commit in commit_list:
            commit_date_time = commit.commit.committer.date
            commit_date = commit_date_time.date()
            if not commit_date > this_day:
                break
            name = commit.commit.committer.name.encode('ascii', 'ignore')

            for user in email_to:
                if name not in user_activity.keys():
                        user_activity[name] = github_body

                if name == user[2] or name == user[1]:
                    commit_url = repo.html + '/commit/' + commit.sha
                    github_body += "<hr/> <b>{0}</b> @ <font color=".format(
                        commit_date_time.strftime("%H:%M"), name)
                    github_body += 'red'
                    github_body += ">{0}</font> <a href='{3}'>{1}</a>\
                                   <br/> {2} <br/>".format(repo.name,
                                                           "comitted",
                                                           commit.sha[:10],
                                                           commit_url)
                    github_body += "<font color='violet'>"
                    github_body += commit.commit.message + "</font><br/>"

                    if github_body:
                        user_activity[name] += github_body
                    github_body = ""

    send_mail(user_activity)
