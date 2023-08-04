import json
import os

def get_resume_by_id(resume_id) :
    with open('Data/resume/'+ str(resume_id) +'.json', 'r') as f:
        resume = json.load(f)
    return resume

def get_all_majors(resume_majors, resume_id) :
    try :
        with open('Data_Translated/resume/'+ str(resume_id) +'_translated.json', 'r') as f:
            resume = json.load(f)

    except FileNotFoundError as e:
        print(f"file resume {resume_id}.json does not exist")
    else :
        print(f"file resume {resume_id}.json was opened successfully.")
        for edu in resume['educations'] :
            if (edu['major'] != None) and (edu['major'].lower() not in resume_majors) :
                resume_majors.append(edu['major'].lower())

    return resume_majors

################################################################
resume_majors = []

for resume_id in range(4287, 5330) :
    resume_majors = get_all_majors(resume_majors, resume_id)

print(resume_majors)

#####################

for major in resume_majors :

    sub_majors = major.split(' ')
    str = ""
    for sub_id in range(len(sub_majors)) :
        if sub_id < len(sub_majors) - 1 :
            str += sub_majors[sub_id] + '-'
        else :
            str += sub_majors[sub_id]

    str_label = '{"label": "MAJOR|DEV MAJOR|' + str + '", "pattern": ['
    for sub_id in range(len(sub_majors)) :
        if sub_id < len(sub_majors) - 1 :
            str_label += '{"LOWER": "' + sub_majors[sub_id] + '"},'
        else :
            str_label += '{"LOWER": "' + sub_majors[sub_id] + '"}]}'

    print(str_label)

    # str_label = '{"label": "MAJOR|AI MAJOR|data-analysis", "pattern": [{"LOWER": "data"}, {"LOWER": "analysis"}]}'
