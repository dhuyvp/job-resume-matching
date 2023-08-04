from Translate import Translate

######################################
# for id in range(5000, 5330) :
for id in range(5150, 5330) :

    trans = Translate()
    trans.translate_json_file_job(id)
    trans.translate_json_file_resume(id)
    
    print(f'Done {id}')