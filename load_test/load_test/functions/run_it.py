#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import grequests
import json
import logging
import logging.handlers
import os
import requests
import shutil
import sys

from subprocess import call
from tempfile import mkdtemp

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

USERS_REPOS_URI = "/user/repos"


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
        os.chdir(repo_dir)

        call ('git init', shell=True)

        logger.debug("Repo directory :: {} ".format(os.getcwd()))

        file_path = '{}/{}'.format(repo_dir, filename)

        with open(file_path, "w") as tmp:
            tmp.write('{} try {}'.format(repo, filename))

        call('git add {}'.format(file_path), shell=True)

        commit_message = "Try {}/{} times".format(repo, repo)
        call('git -c user.name="test" -c user.email="test@email.org" commit -m "{}"'.format(commit_message), shell=True)

        https_git_uri = '{protocol}://{username}:{token}@{hostname}/{user_or_org}/{repo_name}.git'.format(**{
            'protocol': os.environ['GITHUB_PROTOCOL'],
            'username': os.environ['GITHUB_USERNAME'],
            'token': os.environ['GITHUB_TOKEN'],
            'hostname': os.environ['GITHUB_HOSTNAME'],
            'user_or_org': os.environ['GITHUB_USER_OR_ORG_NAME'],
            'repo_name': repo
        })
        logger.debug("Github URI :: {}".format(https_git_uri))
        call('git remote add origin {https_git_uri}'.format(**{
            'https_git_uri': https_git_uri
            }), shell=True)
        call('git push -u origin master', shell=True)
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        logger.info("Cleaning up :: {} ".format(repo_dir))
        os.chdir(old_wd)
        shutil.rmtree(repo_dir)

def main():
    logger.info("being main()")
        
    URI = "{}://api.{}{}".format(os.environ['GITHUB_PROTOCOL'], os.environ['GITHUB_HOSTNAME'], USERS_REPOS_URI)
    logger.info("Using URI :: {}".format(URI))

    header = {
        "Authorization": "token {}".format(os.environ['GITHUB_TOKEN']),
        "Accept": "application/vnd.github.v3.full+json"
    }

    rs = [
        grequests.post(
            URI,
            headers=header,
            data=json.dumps({
                'name': str(repo),
                'description': "This is the {} repo".format(repo),
                'private': False
            }),
            hooks={'response': [hook_factory(repo=repo)]},
            ) for repo in xrange(0, int(os.environ['NUMBER_OF_REPOS']))
    ]

    results = grequests.map(rs)

    for result in results:
        logger.info(result.json())
  
if __name__== "__main__":
    main()
