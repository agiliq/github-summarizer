import sendgrid
import requests

from datetime import date, timedelta

from auth import username, password
from settings import organization, sender, subject


def get_organization_repos(org=organization):
    """
    Retuns all the repos in the given Organization
    """
    url = "https://api.github.com/orgs/{0}/repos"
    repositories = []
    repos = requests.get(url.format(org),
                         params={'type': 'public', 'per_page': '100'},
                         auth=(username, password))
    for repo in repos.json:
        repositories.append(repo['name'])
    return repositories


def get_members(org=organization):
    url = "https://api.github.com/orgs/{0}/members"
    members = []
    member = requests.get(url.format(org),
                          auth=(username, password))
    for memb in member.json:
        members.append(memb['login'])
    return members


def get_user_info(members):
    """
    Takes Github User objects and returns a list of tuples as below.
    [('rakesh@agiliq.com', 'Rakesh Vidya Chandra', 'krvc'),
     ('balu@agiliq.com', 'Bala Subrahmanyam Varanasi', 'Balu-Varanasi'),
    ]
    """
    url = "https://api.github.com/users/{0}"
    user_info = []
    for member in members:
        info = requests.get(url.format(member),
                            auth=(username, password))
        item = info.json['email'], info.json['name'], info.json['login']
        user_info.append(item)
    return user_info

yesterday = date.today() - timedelta(1)


def get_commits(repo):
    """
    Takes a repo and returns the commit list in 'master' branch
    """
    url = "https://api.github.com/repos/agiliq/{0}/commits"
    commits = []
    commit_list = requests.get(url.format(repo),
                               params={'since': yesterday},
                               auth=(username, password))
    for commit in commit_list.json:
        commits.append(commit['commit']['message'])
    return commits


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