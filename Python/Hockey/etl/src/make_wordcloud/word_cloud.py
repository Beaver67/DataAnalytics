import stylecloud
import os


directory = 'data/raw/'
output_dir = 'output/'


def CreateWordcloud(filename, icon, file):
    stylecloud.gen_stylecloud(file_path=filename,
                              icon_name=icon,
                              output_name=file)


for file in os.listdir(directory):
    if file.endswith(".txt"):
        print(os.path.join(directory, file))
        print(os.path.splitext(file)[0]+'.png')
        create_wordcloud(os.path.join(directory, file),
                         "fas fa-apple-alt", output_dir + os.path.splitext(file)[0]+'.png')
        continue
    else:
        continue


# stylecloud.gen_stylecloud(file_path='data/raw/sj-speech.txt',
#           icon_name="fas fa-apple-alt")
