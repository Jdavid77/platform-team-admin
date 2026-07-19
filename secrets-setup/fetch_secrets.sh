#!/usr/bin/env bash
set -eou pipefail

ENV_FILE="../.env"
if [[ ! -f "$ENV_FILE" ]]; then
    echo "Can't find env file...exiting"
    exit 1
fi

set -o allexport
source "$ENV_FILE"
set +o allexport

if ! bw login --check &>/dev/null; then
    bw login --apikey
fi

export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD --raw)

if [ -z "$BW_SESSION" ]; then
    echo "Error: Failed to unlock Bitwarden vault."
    exit 1
fi

github_item=$(bw get item "GitHub Secrets" --session "$BW_SESSION")

github_token=$(echo "$github_item" | jq -r '.fields[] | select(.name == "pulumi-github-token") | .value')
github_owner=$(echo "$github_item" | jq -r '.fields[] | select(.name == "pulumi-github-owner") | .value')

(
    cd ..
    pulumi config set --secret github:token "$github_token"
    pulumi config set github:owner "$github_owner"
)

echo "Pulumi config updated."
