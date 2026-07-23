import yaml
from pulumi import ResourceOptions, export
from pulumi_github import Provider, Repository, Membership, BranchProtection, RepositoryEnvironment, RepositoryEnvironmentReviewerArgs, get_user

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

        branch_protection = BranchProtection(
            f"{repo_name}-main-branch-protection",
            repository_id=repository.name,
            pattern="*",
            enforce_admins=True,
            require_signed_commits=True,
            opts=ResourceOptions(provider=provider, delete_before_replace=True),
        )

        for env_def in repo_def.get("environments", []):
            reviewer_usernames = env_def.get("reviewers", [])
            reviewers = []
            if reviewer_usernames:
                user_ids = [int(get_user(username=u).id) for u in reviewer_usernames]
                reviewers = [RepositoryEnvironmentReviewerArgs(users=user_ids)]

            RepositoryEnvironment(
                f"{repo_name}-{env_def['name']}-environment",
                repository=repo_name,
                environment=env_def["name"],
                reviewers=reviewers,
                opts=ResourceOptions(provider=provider, depends_on=[repository]),
            )

        export(f"{repo_name}_repo_name", repository.name)
