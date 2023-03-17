import aspose.words as aw
def get_filename(file_name,file):

    
    path_pdf = "/home/apprenant/Bureau/NLP_QA_Project/Dataset/{}".format(file_name)
    path_txt = "/home/apprenant/Bureau/NLP_QA_Project/Dataset/{}.txt".format(file_name[:len(file_name)-4])
    file.save(path_pdf)

    doc = aw.Document(path_pdf)
    doc.save(path_txt)

    with open(path_txt, 'r') as f:
        file_content = f.read()
    return file_content()

