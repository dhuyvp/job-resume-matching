import ast
import json
from Resources import DEGREES_IMPORTANCE
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Rules:
    def __init__(self, resumes, jobs):
        with open('Resources/labels.json') as fp:
            labels = json.load(fp)

        self.labels = labels
        self.resumes = resumes
        self.jobs = jobs
        self.degrees_importance = DEGREES_IMPORTANCE

    def modifying_type_resume(self, resumes) :
        resumes['skills'] = ast.literal_eval(resumes['skills'])

        return resumes

    def modifying_type_job(self, jobs) :
        jobs['Skills'] = ast.literal_eval(jobs['Skills'])

        return jobs
    
    ###################################
    # skills matching
    @staticmethod
    def unique_job_skills(job) :
        unique_job_skills = []
        for i in job['Skills'] :
            if i not in unique_job_skills :
                unique_job_skills.append(i)

        return unique_job_skills
    

    def semantic_similarity(self, job, resume):
        if len(resume) == 0 :
            if len(job) == 0 :
                return 0.4
            return 0
        elif len(job) == 0 :
            return 0.5
            #####################333


        model = SentenceTransformer("sentence-transformers/all-roberta-large-v1")
        # model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

        score = 0
        sen = job + resume

        # print('\n\njob before encode: ', job)
        # print('\nresume before encode: ', resume)

        
        sen_embeddings = model.encode(sen)
        # print('\n\n\nsen:', sen, '\n\n\n')
        # print('\n\n\nsen_embeddings:', sen_embeddings.shape, '\n\n\n')
        
        for i in range(len(job)) :
            if job[i] in resume : 
                score += 1
            else :
                if max(cosine_similarity([sen_embeddings[i]], sen_embeddings[len(job):])[0]) >= 0.4 :
                    score += max(cosine_similarity([sen_embeddings[i]], sen_embeddings[len(job):])[0])

        score = score / len(job)
        return round(score, 6)


    def skills_semantic_matching(self, resume, job_index, job_skills) :
        resume['Skills job ' + str(job_index) + ' semantic matching'] = 0
        
        print(job_skills)
        print(resume['skills'])

        resume['Skills job ' + str(job_index) + ' semantic matching'] = self.semantic_similarity(job_skills, resume['skills'])

        return resume

    ########################################
    #degree matching
    @staticmethod
    def assign_degree_matching(match_scores) :
        score = 0
        if (len(match_scores) != 0) :
            if (max(match_scores) >= 2) :
                score = 1
            elif (max(match_scores) >= 0) and (max(match_scores) < 2) :
                score = 0.5
        return score
    
    @staticmethod
    def check_degree_level(self, degree):
        
        for level, degrees in self.labels['DEGREE'].items():
            if degree in degrees:
                return level
        return ''


    def degree_matching(self, resume, job, job_index) :
        job_min_degree = self.degrees_importance[job['Minimum degree level']]

        resume['Degree job ' + str(job_index) + ' matching'] = 0

        # # print(self.check_degree_level(self, 'ba'))

        match_scores = []
        for edu in resume['educations'] :
            score = self.degrees_importance[self.check_degree_level(self, edu['diploma'])] - job_min_degree
            match_scores.append(score)

        # # print('job min degree: ',job_min_degree)

        resume['Degree job ' + str(job_index) + ' matching'] = self.assign_degree_matching(match_scores)

        # # print('check degrees score:', self.assign_degree_matching(match_scores))

        return resume

    ##########################################
    #major matching
    def get_major_category(self, major):
        """get a major's category"""
        categories = self.labels['MAJOR'].keys()
        for c in categories:
            if major in self.labels['MAJOR'][c]:
                return c

    def get_job_acceptable_majors(self, job):
        """get acceptable job majors"""
        job_majors = job['Acceptable majors']
        job_majors_categories = []
        for i in job_majors:
            job_majors_categories.append(self.get_major_category(i))
        return job_majors, job_majors_categories

    def get_major_score(self, resume, job):
        """calculate major matching score for one resume"""
        resume_majors = []
        for edu in resume['educations'] :
            resume_majors.append(edu['major'])

        job_majors, job_majors_categories = self.get_job_acceptable_majors(job)
        major_score = 0
        for r in resume_majors:
            if r in job_majors:
                major_score = 1
                break
            elif self.get_major_category(r) in job_majors_categories:
                major_score = 0.5
        return major_score
    

    def major_matching(self, resumes, jobs, job_index):
        """calculate major matching score for all resumes"""
        resumes['Major job ' + str(job_index) + ' matching'] = 0
        # for i, row in resumes.iterrows():
        resumes['Major job ' + str(job_index) + ' matching'] = self.get_major_score(resumes,jobs)
        return resumes



    #########################################3
    # calculate matching scores
    def matching_score(self, resume, job, job_index):
        #matching skills
        job_skills = self.unique_job_skills(job)
        resume = self.skills_semantic_matching(resume, job_index, job_skills)

        skills_score = 0 \
            + resume['Skills job ' + str(job_index) + ' semantic matching']

        #matching degrees
        resume = self.degree_matching(resume, job, job_index)
        degrees_score = resume['Degree job ' + str(job_index) + ' matching']

        #matching majors
        resume = self.major_matching(resume, job, job_index)
        majors_score = resume['Major job ' + str(job_index) + ' matching']

        return [skills_score, degrees_score, majors_score]
    

#############################################################
