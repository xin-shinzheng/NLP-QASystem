import nltk

path = './training/qadata/questions.txt'
stop_words = set(nltk.corpus.stopwords.words('english'))
def preprocessing(filename):
    """
    Preprocessing the question file
    @param filename:
    @type filename:
    @return:
    @rtype:
    """
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    question_training = []
    with open(filename, 'rt',encoding = 'utf-8-sig') as file:
        for line in file:
            current_line = next(file)
            #if line[0]!='Number':
            word_tokens = tokenizer.tokenize(current_line)
            filter_sent = [word for word in word_tokens if not word in stop_words]
            question_training.append(filter_sent)
            next(file)
    return question_training

# a = preprocessing(path)
# print(a)

#todo: passage retrieval
"""
data structre:  a list of document for each qid , so it will be 50*20 dimension list [[[tokenblock1],[tokenblock2].....20 tokenblocks ],[].....50documents[]]
1. skip qid, read in as xmlfile
2. combine all sentences in <p></p> ( we can do tokenize then extend the list) current the list is only 1d
3. split into 20 blocks --> append each block to the list of document of token blocks 
4. create bag-of-word for each token block
5. computer  the dot similarity for each document mean while find the max number & related index 
6.return the most similar passage (list of 20 tokens)

"""
new_added_stop_words = ['DATE','SECTION','P','LENGTH','HEADLINE','BYLINE','TEXT','DNO','TYPE','SUBJECT','DOC','DOCID','COUNTRY','EDITION','NAME','PUBDATE',
               'DAY','MONTH','PG','COL','PUBYEAR','REGION','FEATURE','STATE','WORD','CT','DATELINE','COPYRIGHT','LIMLEN','LANGUAGE','FILEID','FIRST','SECOND',
                        'HEAD','BYLINE',]
for ele in new_added_stop_words:
    stop_words.add(ele)
filename = './training/qadata/top_docs_test.0'
#test_filename =
def chunks(list, n):
    final_list =[]
    print("start chunks")
    for i in range(0, len(list), n):
        temp_list = list[i:i+n]
        final_list.append(temp_list)
        print("in the chunk")
    return final_list
def document_sep(filename,n=20):
    rank = 0
    doc = []
    candidate_passage = []

    dict_document_tokenblocks ={}
    with open(filename, 'r', encoding='utf-8-sig') as f:
        #large_scale_tokenizer = nltk.RegexpTokenizer(r'\d+,?\d+|\s\w+|\w+\s')
        large_scale_tokenizer = nltk.RegexpTokenizer(r'\w+')
        try:
            current_line = next(f)
            while True:

                #print(current_line)
                if "Rank" in current_line:
                    print("line contains rank: ")
                    print(current_line)
                    numbers = [int(word) for word in current_line.split() if word.isdigit()]
                    if rank != numbers[1]:
                        doc = []
                        rank = numbers[1]
                    #skip <doc>
                    next(f)
                    current_line = next(f)
                    current_docno = current_line.split()[1]
                    dict_document_tokenblocks[current_docno] = []
                    current_line = next(f)
                    print("hi")

                    while "Rank" not in current_line:
                        current_tokens = large_scale_tokenizer.tokenize(current_line)
                        filter_token = [word for word in current_tokens if not word in stop_words]
                        doc.extend(filter_token)
                        current_line=next(f)
                        print("what's up'")
                    print("end of the while loop")
                    candidate_passage = chunks(doc,n)
                    dict_document_tokenblocks[current_docno]=candidate_passage
        except StopIteration:
            print('EOF!')
            candidate_passage = chunks(doc, n)
            dict_document_tokenblocks[current_docno] = candidate_passage
            return dict_document_tokenblocks

    return dict_document_tokenblocks

result = document_sep(filename)
print(result)



    # document separated to lines
            # elif line.startswith("<P>"):
            #     for line in f:
            #         if line.startswith("</P>"):
            #             break
            #         elif line.startswith("<"):
            #             continue
            #         else:
            #             for word in line.split():
            #                 if not word in stop_words:
            #                     doc.append(word)

            # document stored as an entire text
            # there are some other attributes that I did not cover
            # in rank 4/5:
            # <first> <second>, etc.
            # in rank 21:
            # <memo> <Caption> <LeadPara> <Section> needs to be cover
            # also, I think the case where header goes to the next line need to be covered (not sure)
            # code below is covered in the function


            # elif line.startswith("<HL>") or line.startswith("<HEAD>"):
            #     for word in line.split():
            #         if not word in stop_words and (word != "</HL>" or word != "</HEAD>"):
            #             doc.append(word)
            # elif line.startswith("<AUTHOR>"):
            #     for word in line.split():
            #         if not word in stop_words and word != "</AUTHOR>":
            #             doc.append(word)
            # elif line.startswith("<TEXT>"):
            #     next_line = next(f)
            #     # repeated code
            #     # need to make it cleaner if possible
            #     if next_line.startswith("<P>"):
            #         for line in f:
            #             if line.startswith("</TEXT>"):
            #                 break
            #             elif line.startswith("</P>"):
            #                 break
            #             elif line.startswith("<"):
            #                 continue
            #             else:
            #                 for word in line.split():
            #                     if not word in stop_words:
            #                         doc.append(word)
            #
            #     else:
            #         for line in f:
            #             break_flag = False
            #             if line.startswith("</TEXT>"):
            #                 break
            #             elif break_flag:
            #                 break
            #             else:
            #                 for word in line.split():
            #                     if word == "</TEXT>":
            #                         break_flag = True
            #                         break
            #                     else:
            #                         if not word in stop_words:
            #                             doc.append(word)
            #     print(rank)
            #     print(doc)
            # else:
            #     continue


