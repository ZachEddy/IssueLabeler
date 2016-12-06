## Overview
This project serves to automatically label issues and pull requests on GitHub repositories. It accomplishes this task by identifying patterns between issue descriptions and their corresponding labels. With enough user-generated examples for training, it will create meaningful labels on its own. Less time spent labeling = more time for pizza.

## Example
The Rails repository has thousands of labeled issues and pull requests. I collected all ~25,000 of these examples and stored them in `rails_data.json` to use for training. About two-thirds unfortunately don't have labels, which makes them useless for supervised learning. Regardless, the following will demonstrate, in a nutshell, the purpose of this project.

It might help to quickly glance at the [list of labels](https://github.com/rails/rails/labels) used in the Rails repository.

```python
>>> import labeler
>>> lab = labeler.Labeler()
>>> issue = """Some of the rails documentation needs to be updated to match version 4.2.7.1.
... Specifically, they don't include several new methods for model schema"""
>>> l.classify_issue(issue)
[(u'activerecord', u'docs')]
```

After training on several thousand examples, the classifier determines that `issue` should have two labels: `activerecord` and `docs`. This makes a lot of sense considering the language. First, the mention of 'documentation' would suggest it relates to, well, documentation. Second, ModelSchema is a part of ActiveRecord, so it also seems logical to label it `activerecord`.

## Installation
Step 1: clone this repository

        git clone https://github.com/ZachEddy/IssueLabeler

Step 2: install scikit-learn, a machine learning library in Python

        pip install -U scikit-learn




