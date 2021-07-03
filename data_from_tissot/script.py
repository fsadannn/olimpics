import os

for cp,dir,files in os.walk('.'):
    for file in files:
        if file.endswith('.pdf'):
            src = "\""+os.path.join(cp,file)+"\""
            dst = "\""+os.path.join(cp,file[:-4])
            os.system('pdftotext '+src+' '+dst+'.txt"')

