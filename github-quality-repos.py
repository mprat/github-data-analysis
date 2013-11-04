# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#%matplotlib
import requests, json, github, time, itertools
from requests.auth import HTTPBasicAuth
from collections import deque

# <codecell>

# id_rank_list = []
# custom_headers = {'User-Agent': 'mprat'}
# r = requests.get("https://api.github.com/repositories", headers=custom_headers)
# json = r.json()
# r.headers

# <codecell>

# json_return = r.json()
# for repo in json_return:
#     commit_count_params = {'full_name': repo[u'full_name']}
#     commit_count_request = requests.get("https://api.github.com/repos/" + commit_count_params['full_name'])
#     rating = commit_count_request.json()['watchers_count'] + commit_count_request.json()['forks_count'] - commit_count_request.json()['open_issues']/ 5
#     #need to make this binary insert into
#     id_rank[commit_count_params['full_name']] = rating

# <markdowncell>

# Things to take into account: number of contributors, number of downloads?

# <codecell>

# i = 0
# desclen = 1
# while (desclen > 0):
#     desclen = len(r.json()[i][u'description'])
#     i+=1
# print desclen
# print r.json()[i]

# <codecell>

#only keep track of top 5
def rank_insert_into(rating, name, sorted_id_rank, name_list):
    if len(sorted_id_rank) == 0:
        sorted_id_rank.append(rating)
        name_list.append(name)
        return (sorted_id_rank, name_list)
    elif len(sorted_id_rank) < 5:
        return insert_order_helper(rating, name, sorted_id_rank, name_list)
    elif rating <= sorted_id_rank[0]:
        return (sorted_id_rank, name_list)
    else:
        (ranks, names) = insert_order_helper(rating, name, sorted_id_rank, name_list)
        return (ranks[-5:], names[-5:])

def insert_order_helper(rating, name, sorted_id_rank, name_list):
    i = 0
    while (i < len(sorted_id_rank) and rating > sorted_id_rank[i]):
        i+=1
    end_slice_rank = []
    end_slice_name = []
    if i < len(sorted_id_rank):
        end_slice_rank = sorted_id_rank[i:]
        end_slice_name = name_list[i:]
    sorted_id_rank = sorted_id_rank[0:i] + [rating] + end_slice_rank
    name_list = name_list[0:i] + [name] + end_slice_name
    return (sorted_id_rank, name_list)

# <markdowncell>

# The following lines test the `rank_insert_into` method from above.

# <codecell>

# sorted_list = [3, 4]
# name_list = ["a", "b"]
# # (sorted_list, name_list) = rank_insert_into(6, "foo", sorted_list, name_list)
# (sorted_list, name_list) = rank_insert_into(7, "foo", sorted_list, name_list)
# print sorted_list
# print name_list

# <markdowncell>

# Take an iterator (which is like the abstracted PaginatedList of commits) and find the length of it in C-time using deques.

# <codecell>

def count_items_in_iterator(it):
    counter = itertools.count()
    deque(itertools.izip(it, counter), maxlen=0)
    return next(counter)

# <codecell>

def write_to_file(contents, filename):
    with open(filename + ".txt", 'a') as f:
        f.write(contents + "\n")

# write_to_file("test", "one")
# write_to_file("test2", "one")

# <markdowncell>

# What to do next: use pygithub hooks - get all repos and the first time you get a 304 / rate limit exceeded message, get the time until reset, wait until then, and continue.

# <codecell>

g = github.Github("5afa80e8182a9e8f5e0338f203e05a0a6eef9e10")
allrepos = g.get_repos()

# <codecell>

file_to_write_to = "output-10-21-13-full1"

# <codecell>

def try_rating_calc(repo, sorted_rank, sorted_name):
    try:
        rating = repo.watchers_count + count_items_in_iterator(repo.get_commits()) - (repo.open_issues_count / 5.0)
        write_to_file(repo.full_name + ", " + str(rating), file_to_write_to)
        (sorted_rank, sorted_name) = rank_insert_into(rating, repo.full_name, sorted_rank, sorted_name)
        return (sorted_rank, sorted_name)
    except github.GithubException:
        write_to_file("start sleep time = " + str(time.time()), file_to_write_to)
        print zip(sorted_rank, sorted_name)
        time.sleep(60*5)
        write_to_file("end sleep time = " + str(time.time()), file_to_write_to)
        try_rating_calc(repo, sorted_rank, sorted_name)

# <codecell>

all_repos_list = []
i = 0
sorted_rank = []
sorted_name = []
start_time = time.time()
write_to_file("start time = " + str(start_time), file_to_write_to)
for repo in allrepos:
    full_name = repo.full_name
    (sorted_rank, sorted_name) = try_rating_calc(repo, sorted_rank, sorted_name)
#     i += 1
#     if i > 5:
#         break
write_to_file(str(zip(sorted_rank, sorted_name)), file_to_write_to)
write_to_file("total time = "+ str((time.time() - start_time)), file_to_write_to)

# <markdowncell>

# Checked and made sure that the `watchers` tag and the `watchers_count` tag are the same:

# <codecell>

# all_repos_list = []
# i = 0
# for repo in allrepos:
# #     full_name = repo.full_name
#     all_repos_list.append([full_name, repo.watchers, repo.watchers_count])
#     i += 1
#     if i > 10:
#         break
# print all_repos_list

# <codecell>

# print sorted_rank
# print sorted_name

# <codecell>

# a = (1, 2)
# b = ("a", "b")

# <codecell>

# reversed(zip(a, b))

