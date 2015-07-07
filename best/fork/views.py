from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
import sys
import urllib
import json
import time
import os
import operator

def github_time2epoch(string):
    return time.mktime(time.strptime(string, "%Y-%m-%dT%H:%M:%SZ"))

# Create your views here.

@csrf_exempt
def compare(request):
    repo_url = request.POST['name']
    #2. Obtain its forks using the GitHub API
    #2.1. https://api.github.com/repos/USER/REPO/forks (see USER and REPO variables)

    repo_url_list = repo_url.split('/')
    user = repo_url_list[-2]
    repo_name = repo_url_list[-1]

    print "Retrieve: ", "https://api.github.com/repos/" + user + "/" + repo_name + "/forks"
    urllib.urlretrieve("https://api.github.com/repos/" + user + "/" + repo_name + "/forks", "tmp_file.json")

    #2.2. Obtain URL for each fork from the JSON

    with open('tmp_file.json') as data_file:    
        data = json.load(data_file)

    #3. For each fork (including the parent repo):

    forks_dict = {}
    scores_dict = {}

    # Including the original, root repository in the list of forks to be analyzed
    data.append({"owner": {"login": "root"}, "git_url": repo_url + ".git"})
    
# , "created_at": "2010-10-03T00:06:01Z", "pushed_at": "2015-06-03T00:06:01Z"})    

    for fork in data:
        print fork["owner"]["login"], fork["git_url"]
        forks_dict[fork["owner"]["login"]] = fork["git_url"]
#        if github_time2epoch(fork["created_at"]) + 5 < github_time2epoch(fork["pushed_at"]):

        time.sleep(5)
        print "Changed"
        #   3.1 analyze it with Pylint
        os.system("git clone " + fork["git_url"] + " tmp_repository")
        # Obtain Python files
        print "Done"
        python_files = []
        for root, dirs, files in os.walk("tmp_repository"):
            for file in files:
                if file.endswith(".py"):
                     python_files.append(os.path.join(root, file))
        python_files_string = " ".join(python_files)
        command = "pylint --disable=RP0001 --disable=RP0002 --disable=RP0003 --disable=RP0101 --disable=RP0401 --disable=RP0701 --disable=RP0801 " + python_files_string + " > pylint_output.txt"
        os.system(command)
        input = open("pylint_output.txt", "r")
        while 1:
            line = input.readline()
            if not line:
                break
            if "Your code has been" in line:
                score = line.split()[6][:-3]
                print "Score", score
                scores_dict[fork["git_url"]] = float(score)
        input.close()
        os.system("rm -f pylint_output.txt")
        os.system("rm -rf tmp_repository")

    #4. Provide results of the best fork
    print scores_dict

    sorted_by_scores = sorted(scores_dict.items(), key=operator.itemgetter(1))
    sorted_by_scores = sorted_by_scores[::-1]
    html = "<ol>\n"
    for item in sorted_by_scores:
        html += "  <li>" + str(item[0]) + " " + str(item[1]) + "</li>\n"
    html += "</ol>\n"

    template = get_template("main.html")
    rendered = template.render(Context({'results': html}))
    return HttpResponse(rendered)
