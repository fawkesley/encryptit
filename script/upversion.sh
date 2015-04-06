#!/bin/sh -eu

CODE_DIR=$(dirname $0)/../encryptit
VERSION_FILE=${CODE_DIR}/__init__.py


checkout_master() {
    git checkout master
    git pull --ff-only
}

get_current_version() {
    CURRENT_VERSION=$(python -c 'import encryptit; print(encryptit.__version__)')
    echo "Current version: ${CURRENT_VERSION}"
}

prompt_for_new_version() {
    echo "Enter new version (eg 1.2.3) followed by RETURN:"
    read NEW_VERSION
    echo "New version: ${NEW_VERSION}"
}

edit_version_file() {
    sed -i "s/^__version__ = .*$/__version__ = '${NEW_VERSION}'/g" ${VERSION_FILE}
}

commit_and_sign_new_version_file() {
    set -x  # enable command echo
    git add -p ${VERSION_FILE}
    git commit --gpg-sign -m "Upversion ${CURRENT_VERSION} -> ${NEW_VERSION}"
    set +x  # disable command echo
}

make_tag() {
    set -x  # enable command echo
    git tag --sign ${NEW_VERSION} -m "Version ${CURRENT_VERSION}"
    git tag --list
    set +x  # disable command echo
}

instruct_git_push() {
    echo
    echo "In a new shell, verify with:"
    echo "  git log --show-signature"
    echo "  git tag --verify ${NEW_VERSION}"
    echo
    echo "Then press RETURN to push to origin, eg:"
    echo "  git push origin master:master"
    echo "  git push origin --tags"
    read DUMMY
}

push_to_origin() {
    set -x  # enable command echo
    git push origin master:master
    git push origin --tags
    set +x  # disable command echo
}


checkout_master
get_current_version
prompt_for_new_version
edit_version_file
commit_and_sign_new_version_file
make_tag
instruct_git_push
push_to_origin
