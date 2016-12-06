import os
import json
import configuration
import requests

class RepoMiner:
    def __init__(self):
        self.config = configuration.config

    # gathers all the issues for the repository
    def load_issues(self):
        filename = self.config['data_filename']
        if os.path.isfile("json/" + filename):
            print self.overwrite_warning(filename)
            yes = set(['yes','y', 'ye'])
            choice = raw_input().lower()
            if choice not in yes:
                print "Aborting..."
                return
        issues = self.fetch_issues()
        self.write_json_file(filename,issues)
        self.issues = issues

    # warns user when they're about to overwrite
    def overwrite_warning(self,filename):
        return "Warning: '" + filename + "' already exists and will get overwritten if process continues." \
        "\nTo keep file, change 'data_filename' in config.py. Proceed? [y/n]"

    # write a json file to memory
    def write_json_file(self,filename,json_data):
        with open("json/" + filename, 'w') as outfile:
    		json.dump(json_data, outfile, indent=1, sort_keys=True, separators=(',', ':'))

    # remove unused json to reduce size
    def shorten_issue(self,issue):
        shortened = {}
        for key in self.config['tracked_keys']:
            shortened[key] = issue[key]
        return shortened

    # get issues from the github repository via http
    def fetch_issues(self):
        issues = []
        issue_url = self.get_base_url() + "/issues"
        for page_count in range(self.config["max_requests"]):
            print "Progress: sending request " + str(page_count + 1)
            payload = {
                "page": page_count + 1,
                "state": self.config['state'],
                "per_page": self.config['per_page'],
                "access_token": self.config['access_token']
            }
            issues_resp = requests.get(issue_url,params=payload)
            issues_json = json.loads(issues_resp.text)
            if(issues_json == []):
                break
            for issue in issues_json:
                issues.append(self.shorten_issue(issue))
        return issues

    # url of the github repository
    def get_base_url(self):
        return "https://api.github.com/repos/" + self.config['owner'] + "/" + self.config['repo']