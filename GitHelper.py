from git import Repo
import os


class GitHelper():
    def __init__(self, repo):
        self.repo = repo
    def get_by_commit(self, commits):
        files = []
        repo = Repo(self.repo)
        for commit in self.list_args(commits):
            for p,_ in repo.commit(commit).stats.files.items():
                files.append(os.path.join(self.repo,p))
        return list(set(files))

    def list_args(self,commits):
        return list(commits.split(','))



if __name__ == '__main__':
    gitspace = '/Users/phatle/workspace/Python/tools'
    helper = GitHelper(gitspace)
    for f in  helper.get_by_commit('286219002984e101c0fdd5fa1f57d6d59bf07dea'):
        print(f)