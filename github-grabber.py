# Download all GitHub Repos from an Organization given an API Key
# by Sacha Best (@sachabest) - 2/20/15
#
# Requires: OAuth Key (https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
# Requires: simplejson (pip install simplejson)
# Requires: Python 2.7
#
# Usage: github-grabber.py org_name oauth_key local_folder 

import sys
import os
import simplejson as json
import urllib2
import git as git

template_url = 'https://api.github.com/orgs/'
template_token = '/repos?access_token='
template_download = ' /repos/' 
template_repo = '/:repo/:archive_format/:ref'

# json parsing
def grab_repos(url):
	response = urllib2.urlopen(url)
	resp_json = response.read()
	return json.loads(resp_json)

# download repos linked to in json
def download(repo_list, oauth_key, local_folder):
	for repo in repo_list:
		try:
			git.Repo.clone_from('https://' + oauth_key + '@' + repo['clone_url'][8:], os.path.join(local_folder, repo['name']))
			pass
		except Exception, e:
			print 'error cloning ' + repo['name'] + '\n' + str(e)
		else:
			print 'cloned: ' + repo['name']
		finally:
			pass

# main method
def main():
	if len(sys.argv) < 4:
		print 'Usage: github-grabber.py org_name oauth_key local_folder '
		exit()
	oauth_key = sys.argv[2]
	base_url = template_url + sys.argv[1] + template_token + oauth_key
	repo_list = grab_repos(base_url)
	local_folder = sys.argv[3]
	download(repo_list, oauth_key, local_folder)

if __name__ == '__main__':
	main()
