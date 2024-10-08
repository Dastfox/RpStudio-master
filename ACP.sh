#!/bin/bash

# Function to add, commit, and push changes in a submodule
update_submodule() {
    local path=$1
    echo "Updating submodule: $path"
    (
        cd "$path"
        git add .
        if [ -n "$(git status --porcelain)" ]; then
            git commit -m "Update submodule: $path"
            git push origin HEAD:main || git push origin HEAD:master
        else
            echo "No changes in submodule: $path"
        fi
    )
}

# Add and commit changes in the main repository
echo "Updating main repository..."
git add .
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Update main repository and submodules"
else
    echo "No changes in main repository"
fi

# Push changes in the main repository
git push origin HEAD

# Get the list of submodules
submodules=$(git config --file .gitmodules --get-regexp path | awk '{ print $2 }')

# Update each submodule
for submodule in $submodules; do
    update_submodule "$submodule"
done

echo "All updates completed!"