""" main.py

    The main file to run the security scanner checks.

    This code is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
"""

import ConfigParser

import logger
import github
import check

def readConfig(configfile):
    """Read the configuration file. It should contain two parameters: org and token
    
    Keyword arguments:
    configfile -- the file containing the configuration
    """
    config = ConfigParser.ConfigParser()
    config.read(configfile)

    out = {}
    for config_param in ["org", "token"]:
        try:
            out[config_param] = config.get("GitHub", config_param)
        except ConfigParser.NoOptionError:
            print "Could not find the option {}".format(config_param)

    return out

def main():
    """Main function. Read the configuration file, instantiate the GitHub object and run through checks"""

    log = logger.Logger()

    # Read the organization and Oauth token from the configuration file
    log.log("Reading configuration")
    configs = readConfig("config.ini")

    # Instantiate the github object with the organization and Oauth token from the configuratio file
    log.log("Instantiating github object")
    gh = github.GitHub(configs['org'], configs['token'])

    # Test 1: Check users without 2FA
    log.log("Running first check: Check users without 2FA enabled")
    check.check2FA(gh, log)

    # Test 2: Check for invalid commit signatures
    log.log("Running second check: Check Invalid Commit Signatures")
    check.checkCommitSignature(gh, log)

    # Test 3: Check Installed Webhooks
    log.log("Running third check: Check installed webhooks")
    check.checkInstalledWebhooks(gh, log)

    log.log("Running fourth check: Check team member changes")
    check.checkTeamMemberChanges(gh, log)

    # First, loop through all repositories
    #for repo in gh.getAllReposNames():
        #check.checkInvalidSignatures(gh, repo)
        #print repo

# Run main function
if __name__ == "__main__":
    main()

