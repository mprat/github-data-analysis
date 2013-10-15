import github, time

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

def try_rating_calc(repo, sorted_rank, sorted_name):
    try:
        rating = repo.watchers_count
        (sorted_rank, sorted_name) = rank_insert_into(rating, full_name, sorted_rank, sorted_name)
        return (sorted_rank, sorted_name)
    except github.GithubException:
        print "start sleep time = ", time.time()
        print zip(sorted_rank, sorted_name)
        time.sleep(60*5)
        print "end sleep time = ", time.time()
        try_rating_calc(repo, sorted_rank, sorted_name)

if __name__=="__main__":
	g = github.Github()
	allrepos = g.get_repos()
	all_repos_list = []
	i = 0
	sorted_rank = []
	sorted_name = []
	start_time = time.time()
	print "start time = ", start_time
	for repo in allrepos:
		full_name = repo.full_name
		print full_name	
		(sorted_rank, sorted_name) = try_rating_calc(repo, sorted_rank, sorted_name)
		#i += 1
		#if i > 5:
		#	break
	print zip(sorted_rank, sorted_name)
	print "total time = ", time.time() - start_time
