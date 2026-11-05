---
orphan: true
---

# Demo: Git & GitHub

## Basics (via command line)

- sign in to GitHub
- create a new repository:
    - named `sequence` (not to clash with the real `sequences` example that will be used for the rest of the lecture)
    - visibility: public
    - no template
    - add a README
    - choose a Python `.gitignore`
- clone the repository
- make a change
- git add
- git commit -m 'commit message'
  - note: here we are merging to main, as it's the only branch
  - photo book analogy: add = arranging photos, commit = gluing them down
- git push

Now with branches:

- git branch new_feature
- git checkout new_feature
- git branch
  - note: lists all branches, highlights the active one
- make a change, add, commit
- git push -u origin new_feature
  - note: needs `-u` here (unlike the push to main) - cloning only sets up
    tracking for branches that already existed on the remote; `new_feature`
    is brand new, so there's nothing to link to until this first push
- raise and merge the PR in GitHub
- delete the branch on GitHub once merged
- git checkout main
- git pull
- git branch -d new_feature
  - note: deletes the local copy, now that it's merged

## Using VSCode Git integration / un-committed code prevents pulls

- Repeat the branch, change, commit, PR, merge example via VSCode Git integration.
- checkout main
  - make an edit before pull to show git preventing this
  - remove the change, pull, delete the stale branch

## Merge conflicts

- create two new branches off of main:
    - branch 1: change, commit, PR, merge
    - branch 2: change to provoke a conflict, raise PR, resolve in browser via GitHub
- create two new branches off of main:
    - branch 1: change, commit, PR, merge
    - branch 2: change to provoke a conflict, raise PR, resolve in VSCode by merging main into the branch

## GitHub Fork and PR

- [first-contributions](https://github.com/firstcontributions/first-contributions)
 - add name to Contributors.md
 - git commit -m "Add prash to Contributors list"
 - push, raise PR *to the upstream repo*

## GitHub Issue

- make an issue in the `sequence` repo
- possible assignees: current only myself
- invite a student to comment on the issue
- assign the student to the issue

