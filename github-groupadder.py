# Add members to groups for a csv file for matted: gusername, group# \n
# by Sacha Best (@sachabest) - 3/23/15
#
# Requires: OAuth Key (https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
# Requires: simplejson (pip install simplejson)
# Requires: Python 2.7
#
# Usage: github-groupadder.py org_name csv_file oauth_key

import sys
import os
import simplejson as json
import httplib
import urllib
import urllib2
import requests
import csv

# PUT /teams/:id/memberships/:username
template_url = 'https://api.github.com'
orgs_url = '/orgs/';
teams_url = '/teams'
memberships_url = '/memberships/'

def map_names_ids(token, org_name):
	# to kill pagination assume 500 repos max - change to whatever
	url = template_url + orgs_url + org_name + teams_url + '?per_page=500'
	headers = {'Authorization': ' token ' + token, 'Content-type': 'application/json', 'Accept': 'application/vnd.github.v3+json'}
	r = requests.get(url, headers=headers)
	json_result = json.loads(r.text)
	team_map = dict()
	for team_data in json_result: team_map[team_data['name']] = team_data['id']
	return team_map

def add_member(token, org_name, team_map, username, team_number):
	headers = {'Authorization': ' token ' + token, 'Content-type': 'application/json', 'Accept': 'application/vnd.github.v3+json'}
	team_id = team_map[team_number]
	add_member_url = template_url + orgs_url + org_name + teams_url + str(team_id) + memberships_url + username
	r = requests.put(add_member_url, headers=headers)
	print(r.text)

def parse_csv(token, org_name, csv_file):
	reader = csv.reader(csv_file)
	team_map = map_names_ids(token, org_name)
	for row in reader: 
		print(row)
		add_member(token, org_name, team_map, row[0], 'Group' + row[1])

# main method
def main():
	if len(sys.argv) < 4:
		print 'Usage: github-groupadder.py org_name csv_file oauth_key'
		exit()
	org_name = sys.argv[1]
	oauth_key = sys.argv[3]
	csv_filename = sys.argv[2]
	#auth_req = urllib2.Request(auth_url + oauth_key)
	#auth_res = urllib2.urlopen(auth_req)
	csv_file = open(csv_filename, 'r');
	parse_csv(oauth_key, org_name, csv_file)

if __name__ == '__main__':
	main()