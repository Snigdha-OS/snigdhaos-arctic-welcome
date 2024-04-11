#!/bin/bash

# Set the repository URL and branch
REPO_URL="https://github.com/Snigdha-OS/snigdhaos-welcome.git"
BRANCH="master"  # or "main" depending on your repository's default branch

# Commit message
MESSAGE="⏳ @eshanized updated the repository!!!"

# Add all files, commit, and push changes
git add .
git commit -m "$MESSAGE"
git push origin $BRANCH
