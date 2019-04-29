import random
#
# students= [
#     {
#         "name": "Michael",
#         "email": "Student 1",
#         "all_classes": {"CS 320": -1, "CS 440": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 2",
#         "all_classes": {"CS 112": -1, "CS 330": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 3",
#         "all_classes": {"CS 112": -1, "CS 591": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 4",
#         "all_classes": {"CS 506": -1, "CS 440": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 5",
#         "all_classes": {"CS 112": -1, "CS 440": -1, "CS 131": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 6",
#         "all_classes": {"CS 112": -1, "CS 440": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 7",
#         "all_classes": {"CS 391": -1, "CS 440": -1, "CS 210": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 8",
#         "all_classes": {"CS 112": -1, "CS 111": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 9",
#         "all_classes": {"CS 112": -1, "CS 108": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 10",
#         "all_classes": {"CS 210": -1, "CS 440": -1, "CS 460": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 11",
#         "all_classes": {"CS 112": -1, "CS 440": -1, "CS 560": -1},
#     },
#     {
#         "name": "Michael",
#         "email": "Student 12",
#         "all_classes": {"CS 507": -1, "CS 440": -1, "CS 460": -1},
#     },
# ]
#
# all_groups = {} # Ex: {'12342342': ["user1", "user2", "user3", "user4"]}

# Iterate through the students
# If a student has a -1 as a value in all_classes, select them
# Check to see if other students have a group id (not -1) for that class
# If they do, see if that group they're in has an open spot
# If it does, add them and procede
# Else, make a new group


def find_matches(students, all_groups):
    for i in range(len(students)): # Each student
        curr_classes = list(students[i]["all_classes"].keys()) # Get the students classes
        for x in curr_classes: # Check each class the student is enrolled in
            if students[i]["all_classes"][x] == -1: # Needs a match
                found_match = False # Make a checkpoint flag
                for j in range(len(students)): # Check the other students
                    if j == i:
                        continue
                    other_classes = list(students[j]["all_classes"].keys()) # Classes of the other student
                    if found_match:
                        break
                    for y in other_classes:
                        if x == y:
                            other_curr_match = students[j]["all_classes"][y]
                            if other_curr_match != -1:
                                is_room = (len(all_groups[other_curr_match]) < 4)
                                if is_room:
                                    all_groups[other_curr_match].append(students[i]["email"])
                                    students[i]["all_classes"][x] = other_curr_match
                                    found_match = True
                                    break
                if found_match == False:
                    new_group = random.randint(1,100000)
                    while new_group in list(all_groups.keys()):
                        new_group = random.randint(1,100000)
                    all_groups[new_group] = [students[i]["email"]]
                    students[i]["all_classes"][x] = new_group
    return students, all_groups




def print_pretty(students):
    for s in students:
        print(s)

def print_groups(groups):
    for g in list(groups.keys()):
        print(g, groups[g])

# students, all_groups = find_matches(students)
# print_pretty(students)
# print_groups(all_groups)













# def find_matches():
#     for student in studentsA:
#         if student["is_free"]:
#             index = 0
#             while index < len(student["free_times"]):
#                 look_for = student["free_times"][index]
#                 for other_student in studentsB:
#                     if other_student["name"] not in student["proposed_to"] and other_student["is_free"] and \
#                                     other_student["free_times"][index] == look_for:
#                         student["proposed_to"].append(other_student["name"])
#                         student["engaged_to"] = other_student["name"]
#                         other_student["engaged_to"] = student["name"]
#                         other_student["is_free"] = False
#                         student["is_free"] = False
#                         break
#                     elif other_student["name"] not in student["proposed_to"] and other_student["free_times"][index] == \
#                             look_for:
#                         temp = other_student["engaged_to"]
#                         temp_name = find_student(temp)
#                         if temp_name["free_times"].index(look_for) == other_student["free_times"].index(look_for):
#                             continue
#                         reset_student(temp)
#                         student["proposed_to"].append(other_student["name"])
#                         student["engaged_to"] = other_student["name"]
#                         other_student["engaged_to"] = student["name"]
#                         other_student["is_free"] = False
#                         student["is_free"] = False
#                         break
#                 #print(student)
#                 if student["engaged_to"] != "":
#                     break
#                 else:
#                     index += 1
#             # if student["engaged_to"] == "":
#             #     for other_student in studentsB:
#             #         if other_student["is_free"]:
#             #             student["proposed_to"].append(other_student["name"])
#             #             student["engaged_to"] = other_student["name"]
#             #             other_student["engaged_to"] = student["name"]
#             #             other_student["is_free"] = False
#             #             student["is_free"] = False
#             #             break
#
# def find_student(name):
#     for x in studentsA:
#         if x["name"] == name:
#             return x
#
# def reset_student(name):
#     for x in studentsA:
#         if x["name"] == name:
#             x["engaged_to"] = ""
#             x["is_free"] = True
#             return x
#
# def found_matches():
#     for x in studentsA:
#         if x["engaged_to"] == "":
#             return False
#     return True
#
# def happy_end():
#     print("Resolution:\n")
#     for m in studentsA:
#         first = m["name"]
#         second = m["engaged_to"]
#
#         print("{} <---> {}".format(first, second))
#
#
#
# def main():
#     while(True):
#         if found_matches():
#             return
#         find_matches()
#
#
# main()
# happy_end()
