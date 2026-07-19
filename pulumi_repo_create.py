import yaml
from pulumi import ResourceOptions, export
from pulumi_github import Provider, Repository


def create_repos(provider: Provider):
    with open("config/platform_team_values.yaml") as f:
        data = yaml.safe_load(f)

    for repo_def in data.get("github_repositories", []):
        repo_name = repo_def.get("name")
        repo_description = repo_def.get("description", "")
        visibility = repo_def.get("visibility", "private")

        repository = Repository(
            repo_name,
            name=repo_name,
            description=repo_description,
            visibility=visibility,
            opts=ResourceOptions(provider=provider),
        )

        export(f"{repo_name}_repo_name", repository.name)
