from Translate import Translate

######################################
for id in range(4750, 5000) :
    trans = Translate()
    trans.translate_json_file_job(id)
    trans.translate_json_file_resume(id)
    
    print(f'Done {id}')