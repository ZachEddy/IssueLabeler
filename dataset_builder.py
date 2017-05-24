import re
import io
import json
import pickle
import os.path
import subprocess
import configuration
from Naked.toolshed.shell import execute_js

class DatasetBuilder:
    def __init__(self, config, overwrite_existing=False):
        self.dataset = None
        self.config = config
        self.config['tracked_keys'].append('codeblocks')
        self.overwrite_existing = overwrite_existing
        self.syntax = {}
        self.num = 0
        self.save_codeblocks()

    def get_dataset(self):
        if not self.dataset:
            self.initialize_dataset()
        return self.dataset

    def save_codeblocks(self):
        data = {'codeblocks': self.get_dataset()['codeblocks']}
        with io.open('codeblocks.json', 'w', encoding='utf-8') as f:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii = False)
            f.write(str_)
            # json_file.write(data)

    def initialize_dataset(self):
        dataset_path = self.config['dataset_directory']
        path = "datasets/" + dataset_path + "/" + dataset_path
        pickle_path = path + ".pkl"
        if not os.path.exists(pickle_path) or self.overwrite_existing:
            issues = self.load_json_from_memory(path + ".json")
            self.dataset = self.build_dataset(issues)
            self.save_dataset_in_memory(pickle_path)
        else:
            self.dataset = self.load_dataset_from_memory(pickle_path)

    def save_dataset_in_memory(self, pickle_path):
        pickle.dump(self.dataset, open(pickle_path, "wb"))

    def load_dataset_from_memory(self, pickle_path):
        return pickle.load(open(pickle_path, "rb"))

    def load_json_from_memory(self, path):
        with open(path) as json_file:
            return json.load(json_file)

    def sanitize_text(self,text):
        if text:
            text = text.strip()
        return text

    def remove_codeblock(self,code):
        return re.sub('```[\w\W\z]*```','', code)

    def build_dataset(self, issues):
        dataset = {}
        tracked_keys = self.config['tracked_keys']
        for key in tracked_keys:
            dataset[key] = []
            print key
        for issue in issues:
            labels = self.format_labels(issue['labels'])
            if not self.valid_issue(issue) or len(labels) == 0:
                continue
            # print str(self.num) + "/"+ str(len(issues)) + " of 9780 - " + str(issue['number'])
            # self.num += 1
            issue['labels'] = labels
            issue['title'] = self.format_title(issue['title'])
            issue['codeblocks'] = self.format_codeblocks(issue['body'])
            issue['body'] = self.format_body(issue['body'])
            if len(issue['labels']) > 0:
                for key in tracked_keys:
					dataset[key].append(issue[key])
        return dataset

    def format_codeblocks(self, body):
        return re.findall('```[\s\S]*?```', body)

    def format_body(self, body):
        body = self.remove_codeblock(body)
        return self.sanitize_text(body)
        # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # codeblocks = self.find_codeblocks(body)
        # for codeblock in codeblocks:
        #     # print "CODEBLOCK"
        #     p = subprocess.Popen(["node", "codeblock_parse/tokenize_code.js", codeblock], stdout=subprocess.PIPE)
        #     stdout, stderr = p.communicate()
        #     stdout = stdout.decode('ascii', 'ignore')
        #     joined = " ".join(stdout.split())
        #     joined = re.sub("['\"]", "", joined)
        #     # print joined
        #     body = self.remove_codeblock(body)
        #     body += self.sanitize_text(joined)
        # print body
        # print
            # language = str(codeblock.split()[0][3:]).lower()
            # if language in self.syntax:
            #     self.syntax[language] += 1
            # else:
            #     self.syntax[language] = 1
            # print codeblock.split()[3:]
            # print codeblock
            # p = subprocess.Popen(["node", "codeblock_parse/tokenize_code.js", codeblock], stdout=subprocess.PIPE)
            # stdout, stderr = p.communicate()
            # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            # print stdout.split()
            # print "........................"
            # print codeblock.split()
            # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        # body = self.remove_codeblock(body)


        # if len(codeblocks) > 0:
            # if
            # return
        # this is where the parsing stuff goess
        # return self.sanitize_text(body)

    def format_title(self, title):
        return self.sanitize_text(title)

    def format_labels(self, labels):
        label_names = []
        ignored_labels = self.config['ignored_labels']
        for label in labels:
            label_name = label['name']
            if label_name not in ignored_labels:
                label_names.append(label_name)
        return set(label_names)

    def valid_issue(self, issue):
        if issue['body'] and issue['title']:
            return True
        return False

    def find_codeblocks(text):
        return re.findall('```[\s\S]*?```', text)

# d = DatasetBuilder(configuration.config, overwrite_existing=False)
# d.get_dataset()
# print d.dataset['body']




