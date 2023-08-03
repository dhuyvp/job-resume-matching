from Translate import Translate

######################################
# for id in range(4297, 4500) :
#     trans = Translate()
#     trans.translate_json_file_job(id)
#     trans.translate_json_file_resume(id)
    
#     print(f'Done {id}')


#4297 : error
for id in range(4297, 4300) :
    trans = Translate()
    trans.translate_json_file_job(id)
    trans.translate_json_file_resume(id)
    
    print(f'Done {id}')