#################################################################
# FILE : ex11.py
# WRITER : orin pour , orin1 , 207377649
# EXERCISE : intro2cs2 ex11 2021
# DESCRIPTION:this file ex11 file
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
import itertools


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms):
        return self._diagnose_helper(self.root, symptoms)

    def _diagnose_helper(self, root, symptoms):
        """

        :param root: a node
        :param symptoms: a list of symptoms
        :return: the diagnose if found, none if not
        """
        # break line> a leaf> return data (illness name)
        if not root.positive_child:
            return root.data
        # if it`s not a leaf
        # if the symptom exist> continue to positive node
        else:
            if root.data in symptoms:
                return self._diagnose_helper(root.positive_child, symptoms)
            # if the symptom not exist> continue to negative node
            else:
                return self._diagnose_helper(root.negative_child, symptoms)

    def calculate_success_rate(self, records):
        """
        :param records: a list of record object
        :return: % success
        """
        # count the number of diagnose success
        counter = 0
        for record in records:
            # if the diagnose is correct
            if self.diagnose(record.symptoms) == record.illness:
                counter += 1
        try:
            return counter / len(records)
        except ZeroDivisionError:
            raise ValueError("0 records")

    def all_illnesses(self):
        dict1 = self._all_illnesses_helper(self.root, {})
        s_dict = {k: v for k, v in
                  sorted(dict1.items(), key=lambda item: item[1],
                         reverse=True)}
        return list(s_dict)

    def _all_illnesses_helper(self, root, dict):
        if not root.positive_child:
            if root.data:
                if root.data in dict:
                    dict[root.data] += 1
                else:
                    dict[root.data] = 1
            return dict
        self._all_illnesses_helper(root.positive_child, dict)
        self._all_illnesses_helper(root.negative_child, dict)
        return dict

    def paths_to_illness(self, illness):
        return self._paths_to_illness_helper(self.root, [], [], illness, 0)

    def _paths_to_illness_helper(self, root, s_lst, lst, illness, counter):
        # if it`s a leaf
        if not root.positive_child and not root.negative_child:
            # if it`s a leaf of the searched illness
            if root.data == illness:
                # append the current path to lst
                lst.append(s_lst[:])
                # need to check!
                if lst[0]:
                    return True
                # need to check!
                # if there is no path
                else:
                    return [[]]
            return False
        if root.positive_child:
            # positive
            # creating the path
            s_lst.append(True)
            self._paths_to_illness_helper(root.positive_child, s_lst, lst,
                                          illness,
                                          counter)
            # backtracking- removing the last item
            s_lst.pop()
        if root.positive_child:
            # negative
            s_lst.append(False)
            self._paths_to_illness_helper(root.negative_child, s_lst, lst,
                                          illness,
                                          counter)
            # backtracking- removing the last item
            s_lst.pop()
        return lst

    def minimize(self, remove_empty=False):
        self._minimize_helper(self.root, remove_empty)

    def _minimize_helper(self, root, bool1):
        if root.positive_child is not None:
            p_lst = self._minimize_helper(root.positive_child, bool1)
            n_lst = self._minimize_helper(root.negative_child, bool1)
            if bool1:
                if p_lst[0] is None:
                    root.data = root.negative_child.data
                    root.positive_child = root.negative_child.positive_child
                    root.negative_child = root.negative_child.negative_child
                    return n_lst
                elif n_lst[0] is None:
                    root.data = root.positive_child.data
                    root.positive_child = root.positive_child.positive_child
                    root.negative_child = root.positive_child.negative_child
                    return p_lst
            if p_lst == n_lst:
                root.data = root.negative_child.data
                root.positive_child = root.negative_child.positive_child
                root.negative_child = root.negative_child.negative_child
                return n_lst
            return p_lst + n_lst + [root.data]
        else:
            return [root.data]


def _most_common_illness(records):
    lst = []
    no_repeat = []
    for rec in records:
        lst.append(rec.illness)
        if rec.illness not in no_repeat:
            no_repeat.append(rec.illness)
    ill = None
    max = 0
    for i in no_repeat:
        count = lst.count(i)
        if count > max:
            ill = i
            max = count
    d = Diagnoser(Node(ill))
    return d


def _checker(records, symptoms):
    for rec in records:
        if type(rec) != Record:
            raise TypeError("this is not record")
    for i in symptoms:
        if type(i) != str:
            raise TypeError("Not string")
    if records == [] and symptoms == []:
        d = Diagnoser(Node(None))
        return d
    if symptoms == []:
        return _most_common_illness(records)
    return "all good"


def build_tree(records, symptoms):
    a = _checker(records, symptoms)
    if a != "all good":
        return a
    root1 = Node(symptoms[0], None, None)
    d = Diagnoser(root1)
    try:
        new_root = _build_symptoms_tree_helper(records, symptoms, d.root, 1)
        return Diagnoser(
            _build_diagnose_tree_helper(symptoms, records, new_root, [], []))
    except TypeError:
        raise TypeError


def _build_symptoms_tree_helper(records, symptoms, root, counter):
    if counter == len(symptoms):
        return root
    # else:
    root.positive_child = Node(symptoms[counter], None, None)
    root.negative_child = Node(symptoms[counter], None, None)
    _build_symptoms_tree_helper(records, symptoms, root.positive_child,
                                counter + 1)
    _build_symptoms_tree_helper(records, symptoms, root.negative_child,
                                counter + 1)
    return root


def best_diagnose(tree_symptoms, records, yes_lst, no_lst, dict1):
    for r in records:
        flag = True
        for s in tree_symptoms:
            # if there is a symptoms that patient said he does`nt has
            if (s in no_lst) and (s in r.symptoms):
                flag = False
                break
            # one or more symptoms that the patient has does`nt appear in
            # the record
            if (s in yes_lst) and (s not in r.symptoms):
                flag = False
                break
        if flag:
            if dict1.get(r.illness):
                dict1[r.illness] += 1
            else:
                dict1[r.illness] = 1
    if dict1:
        # return most likely illness
        return max(dict1, key=dict1.get)
    return None


def _build_diagnose_tree_helper(symptoms, records, root, yes_lst, no_lst):
    # if it`s a leaf
    if not root.positive_child:
        # positive
        diagnose = best_diagnose(symptoms, records, yes_lst + [root.data],
                                 no_lst, {})
        root.positive_child = Node(diagnose, None, None)
        # negative
        diagnose = best_diagnose(symptoms, records, yes_lst,
                                 no_lst + [root.data], {})
        root.negative_child = Node(diagnose, None, None)
        return root
    # if it`s not a leaf
    else:
        _build_diagnose_tree_helper(symptoms, records, root.positive_child,
                                    yes_lst + [root.data], no_lst)
        _build_diagnose_tree_helper(symptoms, records, root.negative_child,
                                    yes_lst, no_lst + [root.data])
    return root


def optimal_tree(records, symptoms, depth):
    set_symptoms = set(symptoms)
    if len(set_symptoms) != len(symptoms):
        raise ValueError("f")
    if depth < 0 or (len(symptoms)) < depth:
        raise ValueError(
            "make sure that  0 ≥ depth ≥ len(symptoms) and that there is no double symptom")
    # if symptoms is empty list
    if not symptoms:
        return _most_common_illness(records)
    # if depth is 0
    if depth == 0:
        return _most_common_illness(records)
    for rec in records:
        if type(rec) != Record:
            raise TypeError("this is not record")
    for i in symptoms:
        if type(i) != str:
            raise TypeError("Not string")
    best_tree, best_score = Diagnoser, 0
    perm = list(itertools.combinations(symptoms, depth))
    for p in perm:
        tree = build_tree(records, p)
        score = tree.calculate_success_rate(records)
        if score > best_score:
            best_score = score
            best_tree = tree
    return best_tree


records = [Record("influenza", ["cough", "fever"]),
           Record("indigestion", ["stomachache"])]
# optimal_tree(records + ["non_record_type"], ["fever", "cough"], 1)
# optimal_tree(records, ["1", 1], 1)
# optimal_tree(records, ["1"], -1)
# optimal_tree(records, ["1"], 2)
# optimal_tree(records, ["1", "1"], 1)
if __name__ == "__main__":
    #
    # # Manually build a simple tree.
    # #                cough
    # #          Yes /       \ No
    # #        fever           healthy
    # #   Yes /     \ No
    # # covid-19   cold
    #
    flu_leaf = Node("covid-19", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)
    #
    # # Simple test
    # diagnosis = diagnoser.diagnose(["cough"])
    # if diagnosis == "cold":
    #     print("Test passed")
    # else:
    #     print("Test failed. Should have printed cold, printed: ", diagnosis)

    # records1 = parse_data("tiny_data1.txt")
    # print(diagnoser.calculate_success_rate(records1))
    # print(diagnoser.all_illnesses())
    # print(diagnoser.paths_to_illness("covid-19"))
    # # print(check_depth(cold_leaf,1))
    # # print(create_all_path(root))
    # # records1 = parse_data("tiny_data.txt")
    # # tree1 = build_tree(records1, ["headache", "fever", "cough"])
    # # print(best_diagnose(["headache", "fever", "cough"], records1, ["cough"], {}))
    # records = parse_data(r"medium_data1.txt")
    # tree3 = build_tree(records, ["fever", "cough"])
    # print("influenza" == tree3.root.positive_child.positive_child.data,
    #       "meningitis" == tree3.root.positive_child.negative_child.data,
    #       "cold" == tree3.root.negative_child.positive_child.data,
    #       "healthy" == tree3.root.negative_child.negative_child.data)
    # record1 = Record("influenza", ["cough", "fever"])
    # record2 = Record("cold", ["cough"])
    # records = [record1, record2]
    # b = build_tree(records, ["fever"])
    # d = optimal_tree(records, ["cough", "fever"], 1)
    # # issue!
    # # d = optimal_tree(records, ["cough", "fever"], 0)
    #
    # a_leaf = Node("healthy", None, None)
    # b_leaf = Node("cold", None, None)
    # a_vertex = Node("fever", a_leaf, b_leaf)
    # c_leaf = Node("healthy", None, None)
    # d_leaf = Node("cold", None, None)
    # b_vertex = Node("fever", c_leaf, d_leaf)
    # root1 = Node("cough", a_vertex, b_vertex)
    # e_leaf = Node("healthy", None, None)
    # f_leaf = Node("cold", None, None)
    # c_vertex = Node("fever", e_leaf, f_leaf)
    # g_leaf = Node("healthy", None, None)
    # h_leaf = Node("cold", None, None)
    # d_vertex = Node("fever", g_leaf, h_leaf)
    # root2 = Node("cough", c_vertex, d_vertex)
    # root = Node("headache", root1, root2)
    # tree4 = Diagnoser(root)
    # m_tree4 = tree4.minimize(False)
    #
    # a_leaf = Node("healthy", None, None)
    # b_leaf = Node("cold", None, None)
    # a_vertex = Node("fever1", a_leaf, b_leaf)
    # c_leaf = Node("healthy", None, None)
    # d_leaf = Node("cold", None, None)
    # b_vertex = Node("fever", c_leaf, d_leaf)
    # root1 = Node("cough", a_vertex, b_vertex)
    # e_leaf = Node("healthy", None, None)
    # f_leaf = Node("cold", None, None)
    # c_vertex = Node("fever", e_leaf, f_leaf)
    # g_leaf = Node("healthy", None, None)
    # h_leaf = Node("cold", None, None)
    # d_vertex = Node("fever", g_leaf, h_leaf)
    # root2 = Node("cough", c_vertex, d_vertex)
    # root = Node("headache", root1, root2)
    # tree6 = Diagnoser(root)
    # m_tree6 = tree4.minimize(False)
    #
    # a_leaf = Node("strep", None, None)
    # b_leaf = Node("covid-19", None, None)
    # a_vertex = Node("fever", a_leaf, b_leaf)
    # c_leaf = Node("strep", None, None)
    # d_leaf = Node(None, None, None)
    # b_vertex = Node("fever", c_leaf, d_leaf)
    # root = Node("cough", a_vertex, b_vertex)
    # tree5 = Diagnoser(root)
    # m_tree5 = tree5.minimize(True)
    # pass
    # root6 = Node("cold", None, None)
    # diagnoser6 = Diagnoser(root6)
    # paths4 = diagnoser6.paths_to_illness("cold")
    # assert [[]] == paths4, paths4
