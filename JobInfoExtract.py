from spacy.lang.en import English
from Resources import DEGREES_IMPORTANCE
import json

class JobInfoExtract :
    def __init__(self, skills_patterns_path, majors_patterns_path, degrees_patterns_path, job):
        # self.job = job['requirements']

        self.job = job
        self.skills_patterns_path = skills_patterns_path
        self.majors_patterns_path = majors_patterns_path
        self.degrees_patterns_path = degrees_patterns_path
        self.degrees_importance = DEGREES_IMPORTANCE
    
    @staticmethod
    def match_skills_by_spacy(self, job) :
        nlp = English()
        patterns_path = self.skills_patterns_path
        ruler = nlp.add_pipe("entity_ruler")
        ruler.from_disk(patterns_path)
        # Process some text
        doc1 = nlp(job)
        job_skills = []
        for ent in doc1.ents:
            labels_parts = ent.label_.split('|')
            if labels_parts[0] == 'SKILL':
                print((ent.text, ent.label_))
                if labels_parts[1].replace('-', ' ') not in job_skills:
                    job_skills.append(labels_parts[1].replace('-', ' '))

        print('match_skills_by_spacy:', job_skills)

        return job_skills


    @staticmethod
    def match_majors_by_spacy(self, job) :
        nlp = English()
        #Add pattern to the matcher
        patterns_path = self.majors_patterns_path
        ruler = nlp.add_pipe("entity_ruler")
        ruler.from_disk(patterns_path)
        # Process some text
        doc1 = nlp(job)
        acceptable_majors = []
        for ent in doc1.ents:
            labels_parts = ent.label_.split('|')
            if labels_parts[0] == 'MAJOR':
                if labels_parts[2].replace('-', ' ') not in acceptable_majors:
                    acceptable_majors.append(labels_parts[2].replace('-', ' '))
                if labels_parts[2].replace('-', ' ') not in acceptable_majors:
                    acceptable_majors.append(labels_parts[2].replace('-', ' '))
        
        print('acceptable majors:', acceptable_majors)
        
        return acceptable_majors

   
    @staticmethod
    def match_degrees_by_spacy(self, job):
        nlp = English()
        # Add the pattern to the matcher
        patterns_path = self.degrees_patterns_path
        ruler = nlp.add_pipe("entity_ruler")
        ruler.from_disk(patterns_path)
        # Process some text
        doc1 = nlp(job)
        degree_levels = []
        for ent in doc1.ents:
            labels_parts = ent.label_.split('|')
            if labels_parts[0] == 'DEGREE':
                print((ent.text, ent.label_))
                if labels_parts[1] not in degree_levels:
                    degree_levels.append(labels_parts[1])
        
        print('match_degrees_by_spacy:', degree_levels)

        return degree_levels


    @staticmethod
    def get_minimum_degree(self, degrees):
        """get the minimum degree that the candidate has"""
        d = {degree: self.degrees_importance[degree] for degree in degrees}
        return min(d, key=d.get)

    # @staticmethod
    def extract_entites(self, job) :
        job['Minimum degree level'] = ""
        job['Acceptable majors'] = ""
        job['Skills'] = ""

        #### extract info
        requiJob = job['requirements'].replace('. ', ' ')
        degrees = self.match_degrees_by_spacy(self, requiJob)
        if (len(degrees) != 0) :
            job['Minimum degree level'] = self.get_minimum_degree(self, degrees)
        else :
            job['Minimum degree level'] = ""

        job['Acceptable majors'] = self.match_majors_by_spacy(self, requiJob)
        job['Skills'] = self.match_skills_by_spacy(self, requiJob)

        for skill in job['required_skills'] :
            if skill not in job['Skills']:
                job['Skills'].append(skill)

        print('extract entities:', job)

        return job

###########################################################
