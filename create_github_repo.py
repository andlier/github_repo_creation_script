import argparse
from github import Github

#list of allowed prefixes for repos
#p - project
#s - software
#h - hardware
#u - utilities/scripts etc.
#lib - libraries, reusable stuff
#feel free to add to this list as needed

repo_type_list = ['p', 's', 'h', 'u', 'lib']

#github token, create your own from the settings page in github
token = "INSERT_USER_TOKEN_HERE"

#init argparser
parser = argparse.ArgumentParser(description='Create new github repo.')

parser.add_argument('-t', '--type', action='store', dest='type', required=True, choices=repo_type_list,
                    help='Initial character of repo name indicating type of repository.')

parser.add_argument('-n', '--name', action='store', dest='name', required=True,
                    help='Repo name after numbering and type indication.')

parser.add_argument('-d', '--description', action='store', dest='description', required=True,
                    help='Description of repository content.')

results = parser.parse_args()

#initialize github object
g = Github(token)

#init existing repo dict
existing_repo_list = {}
for element in repo_type_list:
    existing_repo_list[element] = []

#iterate through existing repos and add all numbers for a prefix to lists in prefix-dictionary
for repo in g.get_user().get_repos():
    repo_name = repo.name.encode('ascii','ignore')

    #check if repo name starts with one of the allowed prefixes
    if len([prefix for prefix in repo_type_list if repo_name.startswith(prefix)]) > 0:
        #find number after prefix but before first underscore
        repo_number = filter(str.isdigit, repo_name.split('_')[0])
        
        if repo_number != '':
            #if number is found, add to list of repo numbers for that prefix
            existing_repo_list[[prefix for prefix in repo_type_list if repo_name.startswith(prefix)][0]].append(int(repo_number))

#check for spaces in repo name, which is a hassle
if ' ' in results.name:
    print("repo name cannot contain spaces, use _ (underscore) instead.")
    exit()

#check if repo with that prefix exists from before and if it does, up number by 1
if len(existing_repo_list[results.type])>0:
    new_repo_number = max(existing_repo_list[results.type])+1
else:
    new_repo_number = 1

#form name for new repo
new_repo_name = "{0}{1}_{2}".format(results.type, str(new_repo_number).zfill(3), results.name)

#ask if this is the repo name we want
create_repo = raw_input(("Create repo {} ? yes for yes: ".format(new_repo_name))).strip()

#create repo
if create_repo == "yes":
    user = g.get_user()
    created_repo = user.create_repo(new_repo_name, description=results.description)
    print("repo {0} created for user {1}".format(created_repo.name, user.login))
else:
    print("exited without creating repo")
