# visit https://developer.github.com/v3/issues/#parameters to see what
# 'tracked_keys' and 'state' get used for
config = {
    "repo": "rails",
	"owner": "rails",
	"access_token": "[insert access token]",
	"max_requests": 1,
	"per_page": 20,
	"tracked_keys": ["body", "title","number","labels","comments_url"],
    "ignored_labels": ["stale","attached PR","needs feedback","good first patch","needs backport","onhold","pinned","With reproduction steps"],
    "data_filename":"rails_data.json",
    "state":"all"
}