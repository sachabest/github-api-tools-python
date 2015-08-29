# Make groups for up to a given number given an API Key
# by Sacha Best (@sachabest) - 3/20/15
#
# Requires: OAuth Key (https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
# Requires: simplejson (pip install simplejson)
# Requires: Python 3
#
# Usage: github-groupmaker.py org_name oauth_key max_group

import sys
import os
import simplejson as json
import httplib
import urllib
import urllib2
import requests

auth_url = 'https://api.github.com/user?access_token=';
template_url = 'https://api.github.com'
orgs_url = '/orgs/';
teams_url = '/teams'

def post(token, org_name, data):
	print(data)
	url = template_url + orgs_url + org_name + teams_url
	headers = {'Authorization': ' token ' + token, 'Content-type': 'application/json', 'Accept': 'application/vnd.github.v3+json'}
	r = requests.post(url, data=data, headers=headers)
	print(r.text)

def make_team(token, org_name, team_name):
	api_url = template_url + org_name + teams_url
	post_data = dict()
	post_data['name'] = team_name
	#post_data["description"] = ''
	post_data['permission'] = 'push'
	#post_data["repo_name" = []
	json_str = json.dumps(post_data)
	post(token, org_name, json_str)

# main method
def main():
	if len(sys.argv) < 4:
		print 'Usage: github-groupmaker.py org_name oauth_key num_groups'
		exit()
	org_name = sys.argv[1]
	oauth_key = sys.argv[2]
	num_groups = int(sys.argv[3])
	#auth_req = urllib2.Request(auth_url + oauth_key)
	#auth_res = urllib2.urlopen(auth_req)
	for i in xrange(num_groups): make_team(oauth_key, org_name, 'Group' + str(i+1))

if __name__ == '__main__':
	main()