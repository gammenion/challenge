# Part 1

This is the first part of the challenge. All code was written in Python by me, so no boilerplate code.

## Intro

As basic code documentation, `pydoc` was run and the html files under the [docs](./docs) folder were created.

The code is divided into 4 files:
* `main.py`: the main function
* `github.py`: the main class to interact with Github
* `logger.py`: the main class for logging (stdout, syslog, etc)
* `check.py`: module containing the logic for the security scanner checks

To run it, you should have Python 2.7 and the modules requirements installed. To install the dependency modules, run:

```bash
pip install -r requirements.txt
```

Configure the file `config.ini` as the example provided in the file `config.ini.example`.

Then run the scanner by running:

```bash
python main.py
```

### main.py

This is the main script. It is responsible for reading the configuration file in `config.ini`, instantiating the Github object and running the checks.

### github.py

This module interacts with the Github API v3. It is instantiated by passing the organization name and the oauth token to its constructor.

All methods aim to abstract the Github API to be used by the security scanner checks. At the same time, they should try to be as generic as possible for code reuse.

### logger.py

This module takes care of logging. As of now, it is just a basic class that outputs the message with a specific format to `stdout`. The idea is to make this module extensible to many other types of logging system, like a database, syslog (UDP or TCP), etc.

### check.py

This module implements the logic for the checks. Every function is a different check that interacts with the Github module. It is possible to extend this file to include as many checks as necessary.

Initially I was thinking of a plugin system where each check would be a different module inside the folder `plugins` but this would take more time to implement.

### Check 1:

The scanner prints to output all users without 2FA enabled. Having the usernames, it would be easy to extend the functionality to [remove them from the organization](https://developer.github.com/v3/orgs/members/#remove-a-member) and to [move them to another team](https://developer.github.com/v3/orgs/teams/#add-or-update-team-membership).

### Check 2:

The scanner iterates through all repositories of the organization and loops through all their commits. If any commit has a failed verification, it will write to output.

For both checks, a mechanism to alert the security team could be added per check or as a function of the `logger` module.

## Potential extensions

Reviewing installed webhooks is just a call away from the [webhooks API](https://developer.github.com/v3/orgs/hooks/#list-hooks).

Monitoring changes in the team membership throughout multiple scans will require some form of persistence. This can be achieved by storing the results of one scan into a temporary database, be it `sqlite` or a local database server. In the following scan, the results would be checked against what is stored on the database. The way I do this in other projects is by using the module [peewee](http://docs.peewee-orm.com/en/latest/) for easy database to object representation and security manipulation.

## Improvements

This code is far from ready but it shows an initial idea. Regarding the main concerns:

* Complexity: the code is modularized and can be extended without complete refactoring
* Test cases: Unit tests still need to be implemented. The idea for Python testing is creating a framework using the [unittest](https://docs.python.org/2/library/unittest.html) module
* Architecture: the creation of modules and the idea of creating a plugin system is ideal for functionality extension. Modularizing things like logging can prove beneficial for integrating with external monitoring tools or ticketing systems.
* Documentation: the code includes documentation inline, so by running [pydoc](https://en.wikipedia.org/wiki/Pydoc), it automatically generates code documentation.
* Ideas for improvements/extensions: Many concerns about hosting a code repository in the cloud are around how public the repositories are and who has access to the code. Reviewing external collaborations and checking if a repository is public or private is of utmost importance. Checking for SSH key strength or available API keys is also important to ensure that these are revoked once someone leaves the company (for example) and needs to have all access revoked.
* Safety of the application: In a production ready code, more checks for exceptions are required. If the API is unavailable or return bogus answers, the software must be able to continue running in a safe state. Also, if the softare fails, it should avoid logging sensitive information like the oauth token, as this information could be retrieved by other unauthorized parties.

## License

This code is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
