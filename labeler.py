import re
import json
import pprint
import examples
import parse_issue
import configuration
import dataset_builder
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class Labeler:
	def __init__(self):
		self.config = configuration.config
		builder = dataset_builder.DatasetBuilder(self.config, True)
		self.dataset = builder.get_dataset()

		# print self.dataset['body'][0]
		# print self.dataset['labels']

		# self.ignored_labels = set(self.config['ignored_labels'])
		# self.dataset = self.get_dataset()
		# for i in range(len(self.dataset['body'])):
		# 	print i
		# 	print self.dataset['body'][i]

		# # print self.dataset['body'][3]
		#
		# # DON"T ERASE BELOW HERE
		bundle = self.create_classifier()

		#
		self.classifier = bundle['classifier']
		self.binarizer = bundle['binarizer']
		# # ref = 0
		for i in range(40):
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print "Issue url: github.com/rails/rails/issues/" + str(self.dataset['number'][i])
			print "Issue label(s) actual: " + str(self.dataset['labels'][i])
			print "Issue label(s) prediction: " + str(self.classify_issue(self.dataset['body'][i]))

	# classify multiple issues
	def classify_issues(self,issues):
		if type(issues) is list:
			classifications = []
			for issue in issues:
				classifications.append(self.classify_issue(issue))
			return classifications
		print "Input type must be a list"

	# classify single issue
	def classify_issue(self,issue):
		issue = [self.sanitize_text(issue)]
		classification = self.classifier.predict(issue)
		return self.binarizer.inverse_transform(classification)

	# def label_counts(self):
	# 	counts = {}
	# 	for label in self.label_names:
	# 		counts[label] = 0
	# 	for targets in self.dataset['target']:
	# 		for target in targets:
	# 			counts[target] += 1
	# 	print "label => number of issues"
	# 	print
	# 	for key in counts.keys():
	# 		print key + " => " + str(counts[key])

	# create label classifier
	def create_classifier(self):
		binarizer = MultiLabelBinarizer()
		binary_labels = binarizer.fit_transform(self.dataset['labels'])

		estimators = [
			('token', CountVectorizer('english')),
			('tfidf', TfidfTransformer()),
			('classify', OneVsRestClassifier(LinearSVC(random_state=0, class_weight='balanced')))
		]

		classifier = Pipeline(estimators)
		classifier.set_params(
			token__ngram_range = (1,1)
		)
		classifier.fit(self.dataset['body'][40:], binary_labels[40:])
		# joblib.dump(classifier, 'classifier.pkl')
		# joblib.dump(binarizer, 'binarizer.pkl')
		return {"classifier":classifier, "binarizer":binarizer}

	# return a dictionary of individual datum and their labels
	# def get_dataset(self):
	# 	filename = self.config['dataset_directory']
	# 	issues = self.load_json(filename)
	# 	dataset = {}
	# 	for key in self.config['tracked_keys']:
	# 		dataset[key] = []
	# 	for issue in issues:
	# 		issue['body'] = self.sanitize_text(issue['body'])
	# 		issue['title'] = self.sanitize_text(issue['title'])
	# 		issue['labels'] = self.issue_labels(issue)
	# 		if issue['body'] != "" and issue['body'] != None and len(issue['labels']) != 0:
	# 			for key in self.config['tracked_keys']:
	# 				dataset[key].append(issue[key])
	# 	return dataset

	# removes unwanted text from string
	def sanitize_text(self, text):
		if text == None:
			return None
		text = self.remove_codeblock(text)
		text = text.strip()
		return text

	# removes code chunks from using regex
	def remove_codeblock(self,code):
		return re.sub('```[\w\W\z]*```','',code)

	# retrieve labels for an issue
	# def issue_labels(self,issue):
	# 	label_names = []
	# 	for label in issue['labels']:
	# 		label_name = label['name']
	# 		if label_name not in self.ignored_labels:
	# 			label_names.append(label_name)
	# 	return set(label_names)
	#
	# # retreive body text of an issue
	# def issue_data(self,issue):
	# 	data = issue['body']
	# 	if data == None:
	# 		return None
	# 	return self.sanitize_text(data)
	#
	# # load a json file from memory
	# def load_json(self,filename):
	# 	with open("json/" + filename) as json_file:
	# 		return json.load(json_file)
	#
	# # get all the labels from the repository
	# def label_names(self,labels_json):
	# 	names = []
	# 	for json_obj in labels_json:
	# 		names.append(json_obj['name'])
	# 	return names