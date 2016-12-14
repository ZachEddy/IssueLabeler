## Overview
This project attempts to automatically label issues and pull requests on GitHub repositories. It does so by identifying patterns between issue descriptions and their corresponding labels. With enough user-generated examples for training, it will create meaningful labels on its own. Less time spent labeling = more time for pizza 🍕.

## Example
The Rails repository has thousands of labeled issues and pull requests. I collected all ~25,000 and stored them in `rails_data.json` to use for training. About two-thirds unfortunately don't have labels, which makes them useless for supervised learning. Regardless, the following will demonstrate the purpose of this project.

It might help to quickly glance at the [list of labels](https://github.com/rails/rails/labels) used in the Rails repository.

```python
>>> import labeler
>>> l = labeler.Labeler()
>>> issue = """Some of the rails documentation needs to be updated to match version 4.2.7.1.
... Specifically, they don't include several new methods for model schema"""
>>> l.classify_issue(issue)
[(u'activerecord', u'docs')]
```

After training on a few thousand examples, the classifier determines `issue` should have two labels: `activerecord` and `docs`. This makes sense considering the language of the issue. First, mentioning 'documentation' would suggest it relates to, well, documentation. Second, ModelSchema is a part of ActiveRecord, so it seems logical to label it `activerecord`.

I also tested this classifier with 30 labeled issues from the Rails repository. It needs work, but [**the preliminary results are very exciting**](http://chopapp.com/#5a3xiqo0). Seriously, check it out! (the page takes a few seconds to load)

## Installing
You will need **scikit-learn**, a machine learning package for Python. Click [here](http://scikit-learn.org/stable/install.html) to see their step-by-step installation page.

    pip install -U scikit-learn

Clone the repository and you're set!

    git clone https://github.com/ZachEddy/IssueLabeler

## Configuring
Setting this up for different repositories is a matter of modifying `configuration.py`. You will find explanations of each parameter inside [the configuration file](https://github.com/ZachEddy/IssueLabeler/blob/master/configuration.py).

I will quickly mention the need for an access token. GitHub limits unauthenticated users to 60 API requests per hour. With an access token, that limit increases to 5000 per hour. As another measure of rate limiting, GitHub servers won't respond with more than 100 issues per request. You can collect 500,000 issues per hour (more than enough) versus 6000 (probably not enough) by creating an access token. Helpful instructions for generating access tokens are available [here](https://help.github.com/articles/creating-an-access-token-for-command-line-use/).

Once configured, you can collect repository issues with `repo_miner.py`:

```python
>>> import repo_miner
>>> r = repo_miner.RepoMiner()
>>> r.load_issues()
Progress: sending request 1
Progress: sending request 2
Progress: sending request 3
Progress: sending request 4
```

Issues get stored inside the json folder as `.json` files. After the collection process completes, you can follow the example to start classifying on your own.

## Concluding Remarks
If I make the classifier generate labels accurately, I will turn this into a GitHub application that auto-labels new issues via POST requests. At the moment, however, I am working to improving classification.
