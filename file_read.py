import glob

for filename in glob.iglob("templates" + '**/**/**', recursive=True):
     print(filename)