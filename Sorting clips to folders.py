import os
import shutil

start_path = 'documents/private coding/twitch clips/clips'

final_path = 'documents/private coding/twitch clips/sorted_clips'

name_handling_path = 'documents/private coding/twitch clips/scripts/NameCounter'



def name_counter(name_handling_path):

    f = open(name_handling_path, "r")
    read = f.read()
    counter = int(read) + 1

    f = open(name_handling_path, "w")
    f.write (str(counter))
    f.close()

    return counter



def sort_clips(start_path, final_path):

    list_ = os.listdir(start_path)

    compare_list = os.listdir(final_path)

    for file in list_ :

        splitted_name = file.rsplit('_',1)

        if len(splitted_name) == 2:
            
            streamer_name = splitted_name[1] 

            final_name = streamer_name[:-4]
            


        for folder_name in compare_list:


            if folder_name.upper() == final_name.upper():


                clip_number = name_counter(name_handling_path)

                renamed_file = f'{start_path}/{final_name}_{clip_number}.mp4'

                os.rename(f'{start_path}/{file}', renamed_file)

                shutil.move(renamed_file, f'{final_path}/{folder_name}')


                print ('Sucessfully moved the file')

            
            else: 
                
                print ('Could not move the file')
        




sort_clips(start_path, final_path)



