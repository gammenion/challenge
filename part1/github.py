""" github.py

This code is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
"""

try:
    import requests
except ImportError as e:
    print "Import error in github.py. Did you install the requirements? ({})".format(e)

class GitHub():
    """GitHub class: main point of interaction to the Github API"""

    def __init__(self, org, token):
        """Initialization of GitHub class

        Args:
            org (str): Github Organization name to be used
            token (str): Github oauth token for authentication

        Sets:
            self.org (str): Github organization from parameter
            self.token (str): Github authentication token from parameter
            self.url_params (dict): Dictionary containing GET or POST data payload
            self.rate_limit (int): Resets the rate limit control variable
        """
        self.org = org
        self.token = token
        self.url_params = {"access_token": self.token, "per_page": "100"}
        self.rate_limit = 0

#
# User methods
    def getNon2FAMembers(self):
        """Return all members from the org that does not have 2FA enabled
        
        Args:
            None

        Returns:
            A list containing the result of all users without 2FA enabled. Each element of the list contains a dictionary in the format specified here: https://developer.github.com/v3/users/#get-a-single-user
        """

        filt = {"filter": "2fa_disabled"}
        return self._request("orgs/{}/members".format(self.org), params=filt)

    def getAllReposNames(self):
        """Return all repository names of the Organization

        Args:
            None

        Return:
            A list containing the name of all repositories in the organization
        """
        repos = self._request("orgs/{}/repos".format(self.org))
        out = []
        for repo in repos:
            out.append(repo["name"])

        return out

    def getAllReposCommitsSignatures(self, repo):
        """Return all commit SHA hashes of the repository

        Args:
            repo (str): Name of the repository to search for commits

        Return:
            A list of commit hashes as a dictionary containing the SHA and the verification dict
        """
        hashes = self._request("repos/{}/{}/commits".format(self.org, repo))
        out = []
        for _hash in hashes:
            out.append({"sha":_hash["sha"],"verify":_hash["commit"]["verification"]})

        return out

# 
# Internal methods
    def _request(self, path, params={}, method="get", paginate=False):
        """Internal method that creates the HTTP request. It does automatic paging
        
        Args:
            path (str): the path of the github API
            params (dict): all parameters to be passed to the HTTP request (GET or POST) 
            method (str): default "get". Method to be used can be "get" or "post"
            paginate (bool): Check if the request comes from pagination

        Returns:
            Dictionary in the format specified by a specific request (documented in each method executing the _request method)
        """

        if paginate is False:
            request = "https://api.github.com/" + path
            params.update(self.url_params)
        else:
            request = path

        # Get the right function from the requests module for either GET or POST HTTP verbs
        if method == "get":
            func = requests.get
        else:
            func = requests.post
        
        # Set the Accept header to get developer preview
        headers = {
                "Accept":"application/vnd.github.cryptographer-preview"
                }

        # Perform GET or POST request and verify rate limit
        req = func(request, params=params, headers=headers)
        self.rate_limit = req.headers['X-RateLimit-Remaining']

        # Just in case, check rate limit
        if self.rate_limit < 100:
            print "WARNING: Rate limit below 100"

        # Return variable. This will be changed to the return json
        out = True
        if req.status_code == requests.codes.ok:
            # Paginate
            out = req.json()
            if "next" in req.links:
                tmpout = self._request(req.links["next"]["url"], paginate=True)
                out += tmpout

        else:
            req.raise_for_status()

        return out
