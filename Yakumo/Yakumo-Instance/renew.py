import github
orgname = 'HQSPack'
gh = github.Github()
org = gh.get_organization(orgname)
for repo in org.get_repos():
    print(orgname + '/' + repo.name)
    print(repo.clone_url)
