import yaml
from pulumi import ResourceOptions, export
from pulumi_github import Provider, Repository, Membership

# def create_members(provider: Provider):
#     with open("config/platform_team_values.yaml") as f:
#         data = yaml.safe_load(f)

#     for team_member in data.get("github_organization_members", []):
#         name = team_member.get("name")
#         username = team_member.get("github-username")
#         role = team_member.get("github-role", "member")

#     for member in data["github_organization_members"]:
#         username = member["github-username"]
#         role = member["github-role"]

#         team_membership = Membership(
#             f"github-membership-{username}",
#             username=username,
#             role=role,
#         )

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
