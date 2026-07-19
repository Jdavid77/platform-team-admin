import pulumi
from pulumi_github import Provider

from pulumi_repo_create import create_repos

github_provider = Provider(
    "platform-github-provider",
    token=pulumi.Config("github").require("token"),
    owner=pulumi.Config("github").require("owner"),
)

create_repos(github_provider)
