import time
import gzip
from collections import Counter
from itertools import combinations
import sys

start_time = time.time()
first_scan_rules = []
full_data = []
processes = 3
support = 0.4
min_confidence = 0.8
output_path = "Output/Output SON/output_t1.txt"

def get_data_from_file(filename):
    if ".gz" in filename:
        with gzip.open(filename, "rb") as f:
            for line in f:
                list_numbers = map(int,line.decode("ascii").strip().split())
                list_numbers = list(set(list_numbers))
                full_data.append(list_numbers)
    else:
        with open(filename, "rb") as f:
            for line in f:
                list_numbers = map(int,line.decode("ascii").strip().split())
                list_numbers = list(set(list_numbers))
                full_data.append(list_numbers)


def get_chunk_data(k):
    temp_data = list()
    for i in range(len(full_data)):
        if i % processes == k:
            temp_data.append(full_data[i])
    return temp_data

# Function to get unique items list
def get_items_list(sample_data):
    temp_list = list()
    for i in sample_data:
        for j in i:
            # checking for duplicate items
            if j not in temp_list:
                temp_list.append(j)
    return temp_list

def apriori(transactions_list, support):
    final_rules_list = list()
    # Call the function to get unique items in data
    items_list = get_items_list(transactions_list)
    items_list = sorted(items_list)
    support_items_count = int(support * len(items_list))

    # Singleton Candidates dict
    first_candidates_dict = Counter()

    # Counting the total count of each item by counting the item in each basket
    for item in items_list:
        for basket in full_data:
            if(item in basket):
                first_candidates_dict[item]+=1

    # Singleton frequent items
    first_frequent_items_dict = Counter()
    for item in first_candidates_dict:
        if first_candidates_dict[item] >= support_items_count:
            first_frequent_items_dict[frozenset([item])] += first_candidates_dict[item]

    # Now the first frequent set is passed to next candidates dict
    second_candidates_dict = Counter()

    # first making a list of next items to be considered. These are the items from previous frequent itemsets
    next_candidates_set = set() # this is taken to remove duplicates
    temp_frequent_items_list = list(first_frequent_items_dict)
    for i in range(len(temp_frequent_items_list)):
        for j in range(i+1, len(temp_frequent_items_list)):
            doubleton = temp_frequent_items_list[i].union(temp_frequent_items_list[j])
            if len(doubleton) == 2:
                next_candidates_set.add(doubleton)

    next_candidates_list = list(next_candidates_set)

    # counting the next candidates list count. This time each element has two items
    for element in next_candidates_list:
        second_candidates_dict[element] = 0
        for basket in full_data:
            unique_items_each_basket = set(basket)
            # checking if both items is in each basket
            if element.issubset(unique_items_each_basket):
                second_candidates_dict[element] += 1

    # Doubleton frequent itemsets
    second_frequent_items_dict = Counter()
    for item in second_candidates_dict:
        if second_candidates_dict[item] >= support_items_count:
            second_frequent_items_dict[item] += second_candidates_dict[item]

    for itemset in second_frequent_items_dict:
        frequent_item_candidates = [frozenset(item) for item in combinations(itemset, len(itemset) - 1)]
        max_confidence = 0
        for item in frequent_item_candidates:
            first_item = item
            second_item = itemset - first_item
            both_items = itemset
            support_for_first_item = 0
            support_for_second_item = 0
            support_for_both_items = 0 
            for basket in full_data:
                unique_items = set(basket)
                if first_item.issubset(unique_items):
                    support_for_first_item += 1
                if second_item.issubset(unique_items):
                    support_for_second_item += 1
                if both_items.issubset(unique_items):
                    support_for_both_items += 1

            # first item confidence
            current_confidence = support_for_both_items / support_for_first_item * 100
            
            max_confidence = max(max_confidence, current_confidence)

            #second item confidence
            current_confidence = support_for_both_items /support_for_first_item*100
            max_confidence = max(max_confidence, current_confidence)

            if max_confidence >= min_confidence:
                final_rules_list.append((list(first_item)[0], list(second_item)[0]))
    
    return final_rules_list


def SON_Algorithm_on_chunk_data(chunk_data, support_calculated):
    rules = apriori(chunk_data, support_calculated)
    return rules

def SON_Algorithm(k):
    # First step is to get a chunk of data
    chunk_data = get_chunk_data(k)

    if not chunk_data:
        return

    # fraction of chunk data
    p = len(chunk_data) / len(full_data)
    new_support = p * support
    return SON_Algorithm_on_chunk_data(chunk_data, new_support)

def combining_rules_from_each_chunk(first_scan_rules):
    combined_data = list()
    final_combined_data = list()
    for item in first_scan_rules:
        combined_data += item
    for item in combined_data:
        if not item in final_combined_data:
            final_combined_data.append(item)
    return final_combined_data


def checking_result_chunk(temp_result,k):  
    chunk_data = []
    for i in range (len(temp_result)):
        if (i % processes == k):
            chunk_data.append(temp_result[i])
    return chunk_data

def checking_single_process_result(temp_result,k,total_lines):
    result = list()
    temp_list = checking_result_chunk(temp_result,k)
    for pair in temp_list:
        temp_count = 0
        for i in range (len(full_data)):
            first_element = pair[0]
            second_element = pair[1]
            if (first_element in full_data[i] and second_element in full_data[i]):
                temp_count += 1
        if (temp_count/total_lines >= float(support)):
            result.append(pair)
    return result

# default filename
filename = "chess.dat.gz"

try:
    filename = sys.argv[1]
except Exception as e:
    print("No file provided in arguments. It will choose the default file")

get_data_from_file(filename)
total_lines = len(full_data)
for i in range(3):
    first_scan_rules.append(SON_Algorithm(i))

first_temp = []
for res in first_scan_rules:
    first_temp.append(res)  

#Second Scan
result_final_round = []
temp_result = combining_rules_from_each_chunk(first_temp)

for i in range(3):
    result_final_round.append(checking_single_process_result(temp_result, i,total_lines))

final_result = []
for res in result_final_round:
    final_result.append(res)

last_rules = combining_rules_from_each_chunk(final_result)
with open(output_path, "w") as f:
    f.write(f"The SON algorithm for file {filename}\n")
    f.write(str(last_rules))
    f.write("\n")
    f.write(f"The length of rules is {len(last_rules)} \n")
    f.write("\n")
    f.write(f"The program completed in ****** {time.time() - start_time} seconds *************")



