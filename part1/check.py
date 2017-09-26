"""
    check.py

    This file contains all functions necessary for specific checks. This organizes all commands to be included in the main program as separate steps.

    This code is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
"""

import logger

def check2FA(github, logger):
    """Prints all user logins without 2FA enabled"""

    users = github.getNon2FAMembers()
    if len(users) > 0:
        for user in users:
            logger.log(user["login"])

def checkCommitSignature(github, logger):
    """Prints all commit SHA hashes that are not verified"""

    # Collect all repositories from the organization
    repos = github.getAllReposNames()

    # Go through all repositories and collect their commits
    for repo in repos:
        commits = github.getAllReposCommitsSignatures(repo)

        # Run through the commits for that repo and check for false verifies
        for commit in commits:
            sha = commit["sha"]
            verify = commit["verify"]
            if verify["verified"] is False:
                logger.log("{} - {}".format(sha, verify["reason"]))


        # In order to test, just run this once in the first repository returned.
        # In production, this would run in all repositories.
        break

def checkInstalledWebhooks(gh, log):
    """To be developed: Check for installed Webhooks"""
    log.log("TO BE IMPLEMENTED - checkInstalledWebhooks")

def checkTeamMemberChanges(gh, log):
    """To be developed: Check for changes in team membership"""
    # For this check, some kind of persistence is required. 
    log.log("TO BE IMPLEMENTED - checkTeamMemberChanges")
