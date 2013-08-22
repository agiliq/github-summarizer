from datetime import date, timedelta
from dateutil.parser import parse

import requests
import sendgrid

from auth import username, password, sendgrid_auth
from settings import ORGANIZATION, SENDER, SUBJECT
from mailing_list import email_to

yesterday_object = date.today() - timedelta(1)
yesterday = yesterday_object.isoformat()


def get_organization_repos(org=ORGANIZATION):
    """
    Retuns all the repos in the given Organization
    """
    url = "https://api.github.com/orgs/{0}/repos"

    response = requests.get(url.format(org),
                            params={'type': 'all',
                                    'per_page': '100'},
                            auth=(username, password))
    if response.status_code is not 200:
        return []
    return response.json


def get_commits(repo_name):
    """
    Takes a repo and returns the commit list in 'master' branch
    """
    url = "https://api.github.com/repos/agiliq/{0}/commits"
    response = requests.get(url.format(repo_name),
                            params={'since': yesterday},
                            auth=(username, password))
    if response.status_code is not 200:
        return []
    return response.json


def get_last_updated_repos(repositories):
    """
    Takes repositories and returns the repositories that have been
    updated in last 24 hours.
    """
    last_updated_repositories = []
    for repository in repositories:
        last_udpated = parse(repository["updated_at"])
        date_delta = last_udpated.date() - yesterday_object
        if date_delta.days >= 0:
            last_updated_repositories.append(repository)
    return last_updated_repositories


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

    message = sendgrid.Message(SENDER,
                               SUBJECT,
                               "",
                               "<div>" + html + "</div>")
    for person in email_to:
        message.add_to(person[0], person[1])

    sendgrid_obj.smtp.send(message)


user_activity = {}
github_body = ""


def get_user_activity(repo_name, repo_url):

    commit_list = get_commits(repo_name)

    for commit in commit_list:
        email = commit['commit']['committer']['email']

        if email not in email_to.keys():
            continue

        commit_date_time = parse(commit['commit']['committer']['date'])
        name = email_to[email]['full_name']

        if name not in user_activity.keys():
            user_activity[name] = ""

        commit_url = repo_url + '/commit/' + commit["sha"]
        github_body = "<hr/> <b>{0}</b> @ <font color=".format(
            commit_date_time.strftime("%H:%M"), name)
        github_body += 'red'
        github_body += ">{0}</font> <a href='{3}'>{1}</a>\
                       <br/> {2} <br/>".format(repo_name,
                                               "comitted",
                                               commit["sha"][:10],
                                               commit_url)
        github_body += "<font color='violet'>"
        github_body += commit["commit"]["message"] + "</font><br/>"

        if github_body:
            user_activity[name] += github_body
        github_body = ""


organization_repos = get_organization_repos()
recently_updated_repos = get_last_updated_repos(organization_repos)

for repo in recently_updated_repos:
    get_user_activity(repo["name"],
                      repo["html_url"])

send_mail(user_activity)
