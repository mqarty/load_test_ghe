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

USERS_REPOS_URI = "/api/v3/user/repos"


def hook_factory(*factory_args, **factory_kwargs):
    def response_hook(response, *request_args, **request_kwargs):
        directory = factory_kwargs.get('directory')
        repo = factory_kwargs.get('repo')
        return _git_commit_push(directory, repo)
    return response_hook

def _create_git_directory(directory, repo, filename):
    logger.info("_create_git_directory with the following :: {}/{}/{}".format(directory, repo, filename))
    # os.chdir(directory)

    # call ('git init {}'.format(repo), shell=True)
    # call ('cd {}'.format(repo), shell=True)
    # logger.info("Directory :: {}".format(directory))

    # os.chdir(directory+str(repo))
    # call ('pwd', shell=True)
    # call('echo "{} try" > {}'.format(repo, filename), shell=True)
    # call('git add {}'.format(filename), shell=True)

    return "{}{}".format(os.environ['GITHUB_URI'], USERS_REPOS_URI)

def _git_commit_push(directory, repo):
    logger.info("_git_commit_push with the following :: directory={} repo={}".format(directory, repo))
    # os.chdir(directory+str(repo))
    # call('git commit -m "Try {}/{} times"'.format(repo, repo), shell=True)
    # call('git remote add origin git@ghe-dev.sphereci.com:george/{}.git'.format(repo), shell=True)
    # call('git push -u origin master', shell=True)

def main():
    directory = os.getcwd()+"/"    
    number_of_repos = int(os.environ['NUMBER_OF_REPOS'])
    filename =  os.environ['FILENAME'].format(number_of_repos)
    
    header = {"Authorization": "token {}".format(os.environ['TOKEN'])}

    rs = (
        grequests.post(
            _create_git_directory(directory, repo, filename), # removes one for loop
            headers=header,
            data={'name': str(repo)},
            hooks={'response': [hook_factory(directory=directory, repo=repo)]},            
            ) for repo in xrange(0, number_of_repos)
        )
    
    results = grequests.map(rs)

    logger.info(results)

    # Prob should do a cleanup
  
if __name__== "__main__":
    main()
