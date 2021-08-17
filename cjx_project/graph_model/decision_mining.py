import math

def unique_values(rows, col):
    # rows is rdd data type
    # col is used to define attribute
    rdd = set([row[col] for row in rows])
    list_value = (list(rdd))
    return list_value

# Counting the number of rows / label
def class_counts(rows):
    # rows is rdd data type
    counts = {}
    for row in rows:
        if row[-1] in counts:
            counts[row[-1]] += 1
        else:
            counts[row[-1]] = 1
    return counts

# Question is used to check whether row is match condition
class Question:
    def __init__(self, column, value):
        # column is used for define attribute, Ex: column = 0 -> attribute = Humidity
        self.column = column
        # value is feature of attribute, Ex: Sunny, Rain, ...
        self.value = value
        
    def match(self, example):
        # match function is used to compare feature of example matching feature in this question
        # Ex: example[0] = Rain and value in Question = Sunny => return None
        val = example[self.column]
        if val == self.value:
            return example

def partition(rows, question):
    arr = []
    for row in rows:
        if question.match(row) is not None:
            arr.append(row)
            
    return arr

# entropy function is used to get entropy value
def entropy(rows):
    counts = class_counts(rows)
    # counts has form [{'Yes': 12}, {'No': 13}] 
    impurity = 0
    for lbl in counts:    
        prob_of_lbl = counts[lbl] / float(len(rows))
        if prob_of_lbl == 0:
            continue
        impurity -= prob_of_lbl*math.log(prob_of_lbl, 2)
    return impurity


# info_gain function
def info_gain(list_attr_entropy, current_uncertainty):
    return current_uncertainty - sum(list_attr_entropy)


# find_best_split to used to select the best attribute to split dataset
def find_best_split(rows):
    num = len(rows[0]) - 1
    best_gain = 0
    best_attribute = None
    current_uncertainty = entropy(rows)
    # Check whether all samples belong to different label, if current_uncertainty = 0 => 100% sample in same label
    if current_uncertainty != 0:
        for col in range(num):

            values = unique_values(rows, col)
            list_attr_entropy = []
            
            # This loop is used to find entropy for each feature in an attribute
            for val in values:
                question = Question(col, val)
                true_rows = partition(rows, question)
                p = float(len(true_rows) / len(rows))
                list_attr_entropy.append(p*entropy(true_rows))
            
            # Find information gain
            gain = info_gain(list_attr_entropy, current_uncertainty)
            
            #Check which information gain is better
            if gain >= best_gain:
                best_gain = gain
                best_attribute = col
    
    # Value of best_attribute is the order of column 
    return best_gain, best_attribute


# probability is used to count the probability of each label
def probability(counts):
    total = sum(counts.values())
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


# Leaf class is used to store information relating to the prediction value
class Leaf:
    def __init__(self, name, prob):
        self.name = name
        self.prediction = prob


# Branch class is used to store information feature of attribute, and child_node it holds
class Branch_Node:
    nodeid = 0
    def __init__(self, branch, val):
        self.name = 'branch' + str(Branch_Node.nodeid)
        Branch_Node.nodeid += 1
        self.value = val 
        self.branch = branch
        
        if isinstance(branch, Leaf):
            self.value += ' '
            self.value += branch.prediction


# Decision node is used to store tree
class Decision_Node:
    nodeid = 0
    def __init__(self, attribute, list_branches):
        self.name = 'node' + str(Decision_Node.nodeid)
        Decision_Node.nodeid += 1
        self.attribute = attribute
        self.list_branches = list_branches 


# build tree function
def build_tree(rows):
    gain, attribute = find_best_split(rows)
    
    if gain == 0:
        Leafs = []
        counts = class_counts(rows)
        total = sum(counts.values())
        for lbl in counts.keys():
            prob = str(int(counts[lbl] / total * 100)) + "%"
            Leafs.append(Leaf(lbl, prob))
        return Leafs
    
    values = unique_values(rows, attribute)
    
    list_branches = []
    
    # This loop is used to build tree for each feature value of an attribute
    for val in values:
        next_question = Question(attribute, val)
        true_rows = partition(rows, next_question)
        true_branch = build_tree(true_rows)
        if (isinstance(true_branch, list)):
            for branch in true_branch:
                list_branches.append(Branch_Node(branch, val))
        else:
            list_branches.append(Branch_Node(true_branch, val))
    return Decision_Node(attribute, list_branches)


# print_tree is used to visualize tree
def print_tree(node, tree_, headers, isFirstTime=False, rootName=''):
    if isinstance(node, list):
         for leaf in node:
            tree_.node(leaf.name, label=str(leaf.name), shape='oval', color='red')
            if isFirstTime:
                tree_.edge(rootName, leaf.name, label=leaf.prediction, shape='oval', color='red')
    elif not isinstance(node, Leaf):
        tree_.node(node.name, label=headers[node.attribute], shape='diamond', color='orange')
        if isFirstTime:
                tree_.edge(rootName, node.name, label='')
        for node_branch in node.list_branches:
            tree_.edge(node.name, node_branch.branch.name, label = node_branch.value)
            print_tree(node_branch.branch, tree_, headers)
    if isinstance(node, Leaf):
        tree_.node(node.name, label=str(node.name), shape='oval', color='red')