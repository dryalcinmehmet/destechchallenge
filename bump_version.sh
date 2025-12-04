#!/bin/bash

set -eo pipefail

# ---- Cross-platform sed (GNU sed vs BSD sed) ----
sedi() {
    if sed --version >/dev/null 2>&1; then
        sed -i "$@"
    else
        sed -i "" "$@"
    fi
}

PS3='Software Release Type: '
options=("Major" "Minor" "Patch" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Major")
            export RELEASE_TYPE=major
            break;;
        "Minor")
            export RELEASE_TYPE=minor
            break;;
        "Patch")
            export RELEASE_TYPE=patch
            break;;
        "Quit")
            exit;;
        *)
            echo "invalid option $REPLY";;
    esac
done

# Load version from env
workdir="$(pwd)"
export "$(grep 'API_VERSION=' $workdir/.env)"

IFS="."
read -a Arr <<< "$API_VERSION"

PRE_RELEASE_VERSION=$API_VERSION

# Increment version
if [ "$RELEASE_TYPE" == "major" ]; then
    i=${Arr[0]:1}
    declare -i i; i+=1
    Arr[0]="v"$i
    Arr[1]=0
    Arr[2]=0
elif [ "$RELEASE_TYPE" == "minor" ]; then
    i=${Arr[1]}
    declare -i i; i+=1
    Arr[1]=$i
    Arr[2]=0
elif [ "$RELEASE_TYPE" == "patch" ]; then
    i=${Arr[2]}
    declare -i i; i+=1
    Arr[2]=$i
fi

API_VERSION="${Arr[0]}.${Arr[1]}.${Arr[2]}"

rollback() {
    echo "Rolling back version to $PRE_RELEASE_VERSION..."
    sedi "s/^API_VERSION=.*/API_VERSION=$PRE_RELEASE_VERSION/" "$workdir/.env"
    sedi "s/^API_VERSION=.*/API_VERSION=$PRE_RELEASE_VERSION/" "$workdir/.env.dev"
    sedi "s/^API_VERSION=.*/API_VERSION=$PRE_RELEASE_VERSION/" "$workdir/.env.prod"
}

trap rollback INT TERM EXIT

# Update version in env files
sedi "s/^API_VERSION=.*/API_VERSION=$API_VERSION/" "$workdir/.env"
sedi "s/^API_VERSION=.*/API_VERSION=$API_VERSION/" "$workdir/.env.dev"
sedi "s/^API_VERSION=.*/API_VERSION=$API_VERSION/" "$workdir/.env.prod"

trap - INT TERM EXIT

unset API_VERSION
unset PRE_RELEASE_VERSION
