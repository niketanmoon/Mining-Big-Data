import time
import gzip
import random
from collections import Counter
from itertools import combinations
import sys

start_time = time.time()
data = []
items_list = []
final_rules_list = list()
output_path = "Output/Output SRA/output_pumsb_star_ten.txt"
support = 0.2
min_confidence = 0.8

def get_data_from_file(filename):
    with gzip.open(filename, "rb") as f:
        for line in f:
            list_numbers = map(int,line.decode("ascii").strip().split())
            list_numbers = list(set(list_numbers))
            data.append(list_numbers)

def get_random_sample_data(sample_size_percentage, data):
    sample_count = round(len(data) * sample_size_percentage / 100)
    random_sample_data  = random.sample(data, sample_count)
    return random_sample_data

# Function to get unique items list
def get_items_list(sample_data):
    for i in sample_data:
        for j in i:
            # checking for duplicate items
            if j not in items_list:
                items_list.append(j)

# default 
filename = "chess.dat.gz"
size_percentage = 100

try:
    filename = sys.argv[1]
except Exception as e:
    print("No file provided in arguments. It will choose the default file")

try:
    size_percentage = int(sys.argv[2])
except Exception as e:
    print("No percentage provided in arguments. It will choose the default file")

    
get_data_from_file("chess.dat.gz")

# Applying simple randomized algorithm 
sample_size_data = get_random_sample_data(size_percentage, data)



# Call the function to get unique items in data
get_items_list(sample_size_data)
items_list = sorted(items_list)

with open(output_path, "w") as f:
    f.write(f"The randomized algorithm for file {filename}\n")
    f.write("Items List\n")
    f.write(str(items_list))
    f.write("\n")

support_items_count = int(support * len(items_list))

# Singleton Candidates dict
first_candidates_dict = Counter()

# Counting the total count of each item by counting the item in each basket
for item in items_list:
    for basket in data:
        if(item in basket):
            first_candidates_dict[item]+=1
# print("Singleton Candidates table C1:")
# for item in first_candidates_dict:
#     print(str([item])+": "+str(first_candidates_dict[item]))
with open(output_path, "a") as f:
    f.write("Singleton Candidates table C1: \n")
    for item in first_candidates_dict:
        f.write(str([item])+": "+str(first_candidates_dict[item]))
        f.write("\n")
    

# Singleton frequent items
# print()
first_frequent_items_dict = Counter()
for item in first_candidates_dict:
    if first_candidates_dict[item] >= support_items_count:
        first_frequent_items_dict[frozenset([item])] += first_candidates_dict[item]
# print("Singleton frequent items table: ")
# for item in first_frequent_items_dict:
#     print(str(list(item))+": "+str(first_frequent_items_dict[item]))
# print()
with open(output_path, "a") as f:
    f.write("Singleton frequent items table L1: \n")
    for item in first_frequent_items_dict:
        f.write(str(list(item))+": "+str(first_frequent_items_dict[item]))
        f.write("\n")
    f.write("\n")

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
    for basket in data:
        unique_items_each_basket = set(basket)
        # checking if both items is in each basket
        if element.issubset(unique_items_each_basket):
            second_candidates_dict[element] += 1

# print("Doubleton Candidates Table C2: ")
# for item in second_candidates_dict:
#     print(str(list(item))+": "+str(second_candidates_dict[item]))
# print()
with open(output_path, "a") as f:
    f.write("Doubleton Candidates Table C2: ")
    for item in second_candidates_dict:
        f.write(str(list(item))+": "+str(second_candidates_dict[item]))
        f.write("\n")
    f.write("\n")

# Doubleton frequent itemsets
# print()
second_frequent_items_dict = Counter()
for item in second_candidates_dict:
    if second_candidates_dict[item] >= support_items_count:
        second_frequent_items_dict[item] += second_candidates_dict[item]
# print("Doubleton frequent items table: ")
# for item in second_frequent_items_dict:
#     print(f"Item {list(item)} : {second_frequent_items_dict[item]}")
# print()

with open(output_path, "a") as f:
    f.write("Doubleton frequent items table L2: ")
    for item in second_frequent_items_dict:
        f.write(str(list(item))+": "+str(second_frequent_items_dict[item]))
        f.write("\n")
    f.write("\n")

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
        for basket in data:
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
            # print(str(set(first_item))+" -> "+str(set(second_item))+" = "+str(support_for_both_items/support_for_first_item*100)+"%")
            with open(output_path, "a") as f:
                f.write("Rules with confidence: ")
                f.write(str(set(first_item))+" -> "+str(set(second_item))+" = "+str(support_for_both_items/support_for_first_item*100)+"%")
                f.write("\n")

# print("================================")
# print()
# print(final_rules_list)
# print()
# print("=================================")
# print(f"The program completed in ****** {time.time() - start_time} seconds *************")
with open(output_path, "a") as f:
    f.write("\n")
    f.write("Final Rules list \n")
    f.write(str(final_rules_list))
    f.write("\n")
    f.write(f"The length of rules is {len(final_rules_list)//2}")
    f.write("\n")
    f.write(f"The program completed in ****** {time.time() - start_time} seconds *************")


