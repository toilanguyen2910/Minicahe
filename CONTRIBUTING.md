# Contributing to Minicahe

First off, thank you for considering contributing to Minicahe! It's people like you that make Minicahe such a great tool for token compression.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check if there's already an issue open for it. If not, go ahead and open one!

## Fork & create a branch

If this is something you think you can fix, then fork Minicahe and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-new-compression-rule
```

## Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first.

## Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with Minicahe's master branch:

```sh
git remote add upstream git@github.com:toilanguyen2910/Minicahe.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```sh
git checkout 325-add-new-compression-rule
git rebase master
git push --set-upstream origin 325-add-new-compression-rule
```

Finally, go to GitHub and make a Pull Request.

## Code formatting

Please ensure your code is properly formatted before submitting a pull request.
