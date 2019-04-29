studentsA = [
    {
        "name": "Student 1",
        "is_free": True,
        "free_times": ["1", "2", "3", "4", "5", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 2",
        "is_free": True,
        "free_times": ["1", "2", "3", "4", "5", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 3",
        "is_free": True,
        "free_times": ["2", "3", "1", "5", "4", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 4",
        "is_free": True,
        "free_times": ["2", "3", "1", "5", "4", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 5",
        "is_free": True,
        "free_times": ["1", "3", "2", "5", "4", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 6",
        "is_free": True,
        "free_times": ["1", "2", "3", "4", "5", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
]

studentsB = [
    {
        "name": "Student 7",
        "is_free": True,
        "free_times": ["1", "2", "3", "4", "5", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 8",
        "is_free": True,
        "free_times": ["3", "1", "2", "4", "5", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 9",
        "is_free": True,
        "free_times": ["3", "1", "2", "4", "5", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 10",
        "is_free": True,
        "free_times": ["1", "2", "3", "5", "4", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 11",
        "is_free": True,
        "free_times": ["1", "2", "3", "5", "4", "6"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "Student 12",
        "is_free": True,
        "free_times": ["2", "1", "3", "4", "6", "5"],
        "engaged_to": "",
        "proposed_to":[],
    },
]


def find_matches():
    for student in studentsA:
        if student["is_free"]:
            index = 0
            while index < len(student["free_times"]):
                look_for = student["free_times"][index]
                for other_student in studentsB:
                    if other_student["name"] not in student["proposed_to"] and other_student["is_free"] and \
                                    other_student["free_times"][index] == look_for:
                        student["proposed_to"].append(other_student["name"])
                        student["engaged_to"] = other_student["name"]
                        other_student["engaged_to"] = student["name"]
                        other_student["is_free"] = False
                        student["is_free"] = False
                        break
                    elif other_student["name"] not in student["proposed_to"] and other_student["free_times"][index] == \
                            look_for:
                        temp = other_student["engaged_to"]
                        temp_name = find_student(temp)
                        if temp_name["free_times"].index(look_for) == other_student["free_times"].index(look_for):
                            continue
                        reset_student(temp)
                        student["proposed_to"].append(other_student["name"])
                        student["engaged_to"] = other_student["name"]
                        other_student["engaged_to"] = student["name"]
                        other_student["is_free"] = False
                        student["is_free"] = False
                        break
                #print(student)
                if student["engaged_to"] != "":
                    break
                else:
                    index += 1
            # if student["engaged_to"] == "":
            #     for other_student in studentsB:
            #         if other_student["is_free"]:
            #             student["proposed_to"].append(other_student["name"])
            #             student["engaged_to"] = other_student["name"]
            #             other_student["engaged_to"] = student["name"]
            #             other_student["is_free"] = False
            #             student["is_free"] = False
            #             break

def find_student(name):
    for x in studentsA:
        if x["name"] == name:
            return x

def reset_student(name):
    for x in studentsA:
        if x["name"] == name:
            x["engaged_to"] = ""
            x["is_free"] = True
            return x

def found_matches():
    for x in studentsA:
        if x["engaged_to"] == "":
            return False
    return True

def happy_end():
    print("Resolution:\n")
    for m in studentsA:
        first = m["name"]
        second = m["engaged_to"]

        print("{} <---> {}".format(first, second))



def main():
    while(True):
        if found_matches():
            return
        find_matches()


main()
happy_end()
