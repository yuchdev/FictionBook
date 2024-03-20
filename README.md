# FictionBook

FictionBook2 files read and write

## Git Workflow

### Branches

* `master`: Represents the main branch of the repository, where stable production-ready code resides.
* `dev`: Development branch where feature branches are merged for integration and testing.
* Task Branches: Each task or feature is developed on its own branch, named with the ticket number and a brief description, e.g. `task/ticket-123-add-feature-x`.

### Workflow Steps

#### 1. Clone Repository: Clone the repository to your local machine:

```bash
git clone <repo URL>
cd <repo_name>
```

#### 2. Create a New Task Branch
Before starting work on a task, create a new branch from the dev branch:

```bash
git checkout dev
git pull origin dev
git checkout -b task/ticket-123-feature-description
```

#### 1. Work on the Task: Implement the necessary changes, adding, and committing them locally:

```bash
git add .
git commit -m "Implement feature XYZ (TICKET-123)"
```

#### 4. Push the Task Branch

Push the task branch to the remote repository:

```bash
git push origin task/ticket-123-feature-description
```

#### 5. Create Pull Request (PR)

Create a pull request from the task branch to the dev branch via the repository's hosting service. Assign reviewers for code review.

#### 6. Review and Address Feedback

Reviewers provide feedback on the changes. Make necessary adjustments, committing changes to the task branch and pushing them.

#### 7. Merge to `dev`

Once the PR is approved, merge the task branch into the dev branch:

```bash
git checkout dev
git pull origin dev
git merge --no-ff task/TICKET-123-feature-description
git push origin dev
```

#### 8. Prepare for Release

Create a release branch from dev for final testing and adjustments:

```bash
git checkout -b release/v1.0.0
```

#### 9. Merge to master and Tag Release

Once the release branch is stable, merge it into the master branch and tag the release:

```bash
git checkout master
git pull origin master
git merge --no-ff release/v1.0.0
git tag v1.0.0
git push origin master --tags
```

#### 10. Deployment

Deploy the tagged release from the master branch to production.

#### 11. Cleanup

Delete the task branch both locally and remotely after it's merged:
