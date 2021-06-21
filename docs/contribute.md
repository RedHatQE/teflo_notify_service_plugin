# Notify Service Plugin Development Guide

### To return to documentation home page press [here](https://redhatqe.github.io/teflo_notify_service_plugin/index.html).

The plugin team welcomes your contributions to the project. 
Please use this document as a guide to working on proposed changes to Notify Service Plugin. 
We ask that you read through this document to ensure you understand our development model and 
best practices before submitting changes.

## Branch Model
We follow a git-flow type of model. Currently there are two branches
* Develop - where all current work is done
* Main - stable release

Both branches are protected in github. We do not allow commits directly to either branch. Only the maintainers
are allowed to cut a release and request a merge of `develop` into `master`. 
All contributors should create new work branches off the `develop` and request a merge to `develop` when ready. 

## How to setup your development environment
Lets first clone the source code
```bash
git clone https://github.com/RedHatQE/teflo_notify_service_plugin.git

```

Next lets create a Python virtual environment for teflo. This assumes you have virtualenv package installed.
```bash
$ mkdir ~/.virtualenvs
$ virtualenv ~/.virtualenvs/wb_plugin
$ source ~/.virtualenvs/ns_plugin/bin/activate
```

Now that we have our virtual environment created. Lets go ahead and install the Python packages used for development.
```bash
(wb_plugin) $ pip install -r teflo_notify_service_plugin/test-requirements.txt
```

Let’s create our new branch from develop
```bash
(wb_plugin) $ git checkout develop
(wb_plugin) $ git checkout -b <new branch>
```

Finally install the plugin itself using editable mode. This will install teflo for you. 
```bash
(wb_plugin) $ pip install -e teflo_notify_service_plugin/.
```

You can verify teflo is installed by running the following commands.
```bash
(wb_plugin) $ teflo
(wb_plugin) $ teflo --version
```

## How to run tests locally
You can run the unit tests and verify pep8 by the following command:
```bash
(ns_plugin) $ make test-functional
```

This make target is actually executing the following tox environments:
```bash
(ns_plugin) $ tox -e py3-unit
```
We have the following standards and guidelines

* All tests must pass
* Code coverage must be above 50%
* Code meets PEP8 standards
* There should be tests included with the code changes where possible
* There should be documentation included with the code changes where possible

Before any change is proposed to the plugin we ask that you run the tests to verify the above standards. 

If there is a reason that the changes don’t have any accompanying tests we should 
be annotating the code changes with TODO comments with the following information:

* State that the code needs tests coverage
* Quick statement of why it couldn’t be added.

## How to submit a change for review
At this point you have your local development environment setup. 
You made some code changes, ran through the unit tests and pep8 validation. 
Before you submit your changes you should check a few things:

If the develop branch has changed since you last pulled it down it is 
important that you get the latest changes in your branch. You can do that in two ways:

Rebase using the local develop branch
```bash
(ns_plugin) $ git checkout develop
(ns_plugin) $ git pull origin develop
(ns_plugin) $ git checkout <branch>
(ns_plugin) $ git rebase develop

```

or 

Rebase using the remote develop branch
```bash
(ns_plugin) $ git pull --rebase origin/develop
```

If you have multiple commits its best to squash them into a single commit. 
The interactive rebase menu will appear and guide you with what you need to do.
```bash
(ns_plugin) $ git rebase -i HEAD~<the number of commits to latest develop commit>
```

You can push then branch upstream
```bash
(ns_plugin) $ git push -u -f  origin <branch>
```

Finally, to submit the PR you can do :

* Use the Github `new pull request` wizard. Be sure to select the `develop` branch.

The github actions workflow will trigger and run tests. Whether the tests pass or fail the job
will post a comment with a status a url to the build. 

If the job fails,

* Make the changes to your branch and when you push the changes to your branch
the workflow will re-trigger.
