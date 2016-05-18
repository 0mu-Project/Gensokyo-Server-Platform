import github
orgname = 'HQSPack'
gh = github.Github('m85091081','***REMOVED***')
org = gh.get_organization(orgname)
for repo in org.get_repos():
    print(orgname + '/' + repo.name)
    print(repo.clone_url)
