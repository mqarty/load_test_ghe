#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import grequests
import logging
import logging.handlers
import os
import requests
import shutil
import sys

from github import Github
from subprocess import call
from tempfile import mkdtemp

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

USERS_REPOS_URI = "/api/v3/user/repos"


def hook_factory(*factory_args, **factory_kwargs):
    def response_hook(response, *request_args, **request_kwargs):
        repo = factory_kwargs.get('repo')
        return _git_steps(repo)
    return response_hook

def _git_steps(repo):
    repo = str(repo)
    filename =  os.environ['FILENAME'].format(repo)

    logger.info("_git_steps with the following :: {}, {}".format(repo, filename))

    old_wd = os.getcwd()

    try:
        # Fix this section
        repo_dir = mkdtemp()
        r = git.Repo.init(repo_dir)
        commit_message = "Try {}/{} times".format(repo, repo)
        logger.info("Calling GIT commands in {}".format(repo_dir))
        
        with open(path, "w") as tmp:
            tmp.write('{} try" > {}'.format(repo, filename))
            r.index.add([tmp])
            r.index.commit(commit_message)
    finally:
        os.chdir(old_wd)
        shutil.rmtree(repo_dir)

def main():
    logger.info("being main()")
        
    URI = "{}://{}{}".format(os.environ['GITHUB_PROTOCOL'], os.environ['GITHUB_HOSTNAME'], USERS_REPOS_URI)
    logger.info("Using URI :: {}".format(URI))

    header = {"Authorization": "token {}".format(os.environ['GITHUB_TOKEN'])}

    rs = (
        grequests.post(
            URI,
            headers=header,
            data={'name': str(repo)},
            hooks={'response': [hook_factory(repo=repo)]},            
            ) for repo in xrange(0, int(os.environ['NUMBER_OF_REPOS']))
        )
    
    results = grequests.map(rs)

    logger.info(results)
  
if __name__== "__main__":
    main()
