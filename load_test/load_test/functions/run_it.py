#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import requests
import grequests
import logging
import logging.handlers
import os
import requests
import sys

from subprocess import call

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

USERS_REPOS_URI = "/api/v3/user/repos" # /rest/api/2/issue/{issue_key}?expand=changelog"


def _create_git_directory(directory, repo, filename):
    logger.info("_create_git_directory :: {}/{}/{}".format(directory, repo, filename))
    # os.chdir(directory)

    # call ('git init {}'.format(repo), shell=True)
    # call ('cd {}'.format(repo), shell=True)
    # logger.info("Directory :: {}".format(directory))

    # os.chdir(directory+str(repo))
    # call ('pwd', shell=True)
    # call('echo "{} try" > {}'.format(repo, filename), shell=True)
    # call('git add {}'.format(filename), shell=True)

def _git_commit_push(r, *args, **kwargs):
    repo = kwargs.get('repo')
    logger.info("_git_commit_push :: {}".format(repo))
    # call('git commit -m "Try {}/{} times"'.format(repo, repo), shell=True)
    # call('git remote add origin git@ghe-dev.sphereci.com:george/{}.git'.format(repo), shell=True)
    # call('git push -u origin master', shell=True)

def main():
    num = 2
    directory = os.getcwd()+"/"
    filename = "try-num-times.txt".format(num)

    url = "https://ghe-dev.sphereci.com/{}".format(USERS_REPOS_URI)
    header = {"Authorization": "token {}".format(os.environ['TOKEN'])}

    for repo in xrange(0, num):
        _create_git_directory(directory, repo, filename)

    rs = (
        grequests.get(
            url,
            headers=header,
            hooks={'response': _git_commit_push},
            ) for repo in xrange(0, num)
        )
    
    results = grequests.map(rs)

    logger.info(results)
  
if __name__== "__main__":
    main()
