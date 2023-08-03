import json
import os

def get_resume_by_id(resume_id) :
    with open('Data/resume/'+ str(resume_id) +'.json', 'r') as f:
        resume = json.load(f)
    return resume

def get_all_majors(resume_majors, resume_id) :
    try :
        with open('Data/resume/'+ str(resume_id) +'.json', 'r') as f:
            resume = json.load(f)

    except FileNotFoundError as e:
        print(f"file resume {resume_id}.json does not exist")
    else :
        print(f"file resume {resume_id}.json was opened successfully.")
        for edu in resume['educations'] :
            if (edu['major'] != None) :
                resume_majors.append(edu['major'])

    return resume_majors

################################################################
resume_majors = []

for resume_id in range(4287, 5323) :
    resume_majors = get_all_majors(resume_majors, resume_id)

# with open('Data/resume/'+ str(4287) +'.json', 'r') as f:
#     resume = json.load(f)

#     print(resume)

resume_majors = get_all_majors(resume_majors, 4287)

print(resume_majors)