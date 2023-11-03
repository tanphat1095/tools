from git import Repo
from pathlib import Path


class GitHelper():
    def __init__(self, repo):
        self.repo = repo
    def get_by_commit(self, commits):
        files = []
        repo = Repo(self.repo)
        for commit in self.list_args(commits):
            for p,_ in repo.commit(commit).stats.files.items():
                files.append(self.join_path(self.repo,p))
        return list(set(files))

    def list_args(self,commits):
        return list(commits.split(','))

    def join_path(self, *paths):
        return Path(*paths).absolute()

if __name__ == '__main__':
    gitspace = 'D:\Backend\sl02y23dms\sl01y23dms'
    helper = GitHelper(gitspace)
    for f in  helper.get_by_commit('f6d96a271ac7a98ce131712d46bf7505bae22cbd'):
        print(f)