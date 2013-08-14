import sendgrid
from auth import github_auth
from datetime import datetime, timedelta
from dateutil import tz
from pygithub3 import Github
from pygithub3.services.repos import Commits
from mailing_list import email_to


def main():

    gh = Github(login=github_auth[0],
                password=github_auth[1])

    agiliq = gh.users.get('agiliq')
    agiliq_repos = gh.repos.list('agiliq').all()
    local_zone = tz.tzlocal()

    today = datetime.now()
    today = today.replace(tzinfo=local_zone)

    this_day = (today - timedelta(hours=24)).date()
    subject = "Agiliq-Github Summary for the day "
    subject += today.strftime("%b %d %Y")

    github_body = ""
    user_activity = {}

    for repo in agiliq_repos:

        agiliq_commit = Commits(user='agiliq', repo=repo.name)
        commit_list = agiliq_commit.list(sha='master', path=None).all()

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

    html = "<html><body>"
    holiday = True

    for key, value in user_activity.iteritems():
        if value:
            html += "<div>" + "<h3>" + key + "</h3>" + value + "</div>"
            holiday = False
    html += "</body></html>"
    if not holiday:
        message = sendgrid.Message("rakesh@agiliq.com",
                                   subject,
                                   "",
                                   "<div>" + html + "</div>")
        for person in email_to:
            message.add_to(person[0], person[1])
        s.smtp.send(message)

main()
