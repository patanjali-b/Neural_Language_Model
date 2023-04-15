# to make a tokenizer using regex
import sys
import re
import math
import random

choice = sys.argv[1]
path = sys.argv[2]
if(choice == 'k'):
    if(path == 'Pride.txt'):
        address = path
        # print(address)


        text_str = ""
        # Open the file in read mode
        with open(address, 'r') as file:
            # Loop through the lines of the file
            for line in file:
                text_str = text_str + line + " "
        # replace all spaces with a single space
        text_str = re.sub(r'\s+', ' ', text_str)
        # replace all urls with <URL>
        url_pattern = re.compile(r'^https?:\/\/.*[\r\n]*')
        text_str = url_pattern.sub('<URL>', text_str)
        text_str = text_str[1713:-18524]
        # replace all mentions with <MENTION>
        mention_pattern = re.compile(r'@\w+')
        text_str = mention_pattern.sub('<MENTIONNN>', text_str)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        text_str = hashtag_pattern.sub('<HASHTAGGG>', text_str)
        # remove all punctuation marks except period, question mark, exclamation mark
        text_str = re.sub(r'[^\w\s.?!]', '', text_str)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        text_str = re.sub(r'\bdr\.', 'dr', text_str)
        text_str = re.sub(r'\bmr\.', 'mr', text_str)
        text_str = re.sub(r'\bmrs\.', 'mrs', text_str)
        text_str = re.sub(r'\bms\.', 'ms', text_str)
        # remove all numeric characters
        text_str = re.sub(r'\d+', '', text_str)
        # lowercase all letters
        text_str = text_str.lower()
        # remove all underscores
        text_str = re.sub(r'_', '', text_str)

        # split text string into a list of sentences
        sentences = re.split(r'[.?!]', text_str)
        training_sentences = sentences
        # print(sentences)
        testing_sentences = random.sample(training_sentences, 1000)
        training_sentences = [sentence for sentence in sentences if sentence not in testing_sentences]
        # split sentences into a list of words
        words = []
        list_of_sentences = list()
        for sentence in training_sentences:
            local_list = list()
            local_list = (sentence.split())
            list_of_sentences.append(local_list)
        # print(list_of_sentences)

        # creating a one-gram
        one_gram = dict()
        for sentence in list_of_sentences:
            for word in sentence:
                if word in one_gram:
                    one_gram[word] += 1
                else:
                    one_gram[word] = 1
        # print(one_gram)

        # creating a two-gram
        two_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 1):
                key = (sentence[i], sentence[i + 1])
                if key in two_gram:
                    two_gram[key] += 1
                else:
                    two_gram[key] = 1
        # print(two_gram)

        # creating a three-gram
        three_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 2):
                key = (sentence[i], sentence[i + 1], sentence[i + 2])
                if key in three_gram:
                    three_gram[key] += 1
                else:
                    three_gram[key] = 1
        # print(three_gram)

        # creating a four-gram
        four_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 3):
                key = (sentence[i], sentence[i + 1], sentence[i + 2], sentence[i + 3])
                if key in four_gram:
                    four_gram[key] += 1
                else:
                    four_gram[key] = 1


        sum_of_all_one_grams = 0
        for i in (one_gram.values()):
            sum_of_all_one_grams += i
        count_3 = len(three_gram.keys())
        count_2 = len(two_gram.keys())
        # print(sum_of_all_one_grams)


        def get_lambda(n_gram):
            n = len(n_gram)
            # print("here len", n, n_gram, type(n_gram))
            if(n == 2):
                sum = 0
                count = 0
                for i in (three_gram.keys()):
                    if(i[0] == n_gram[0]) and (i[1] == n_gram[1]):
                        sum += three_gram[i]
                        count += 1
                sum = max(sum, 1)
                # print(sum, count)
                return ((0.75/sum) * count)
            
            elif(n == 3):
                sum = 0
                count = 0
                for i in (four_gram.keys()):
                    if(i[0] == n_gram[0]) and (i[1] == n_gram[1]) and (i[2] == n_gram[2]):
                        sum += four_gram[i]
                        count += 1
                sum = max(sum, 1)
            
                return ((0.75/sum) * count)


        def kneyser_ney(n_gram):
            # print(n_gram)
            if(len(n_gram) == 1):
                if(n_gram[0] in one_gram.keys()):
                    # print ("returning")
                    return one_gram.get(n_gram[0], 0) / sum_of_all_one_grams
                else:
                    # print ("returning")
                    return 0.75 / sum_of_all_one_grams

            elif (len(n_gram) == 4):
                if (n_gram[0], n_gram[1], n_gram[2], n_gram[3]) in four_gram.keys():
                    val = four_gram[n_gram[0], n_gram[1], n_gram[2], n_gram[3]]
                else:
                    val = 0
                value = max(0, val - 0.75)
                if(value == 0):
                    val2 = 1
                else:
                    if (three_gram[n_gram[0], n_gram[1], n_gram[2]]) not in three_gram.keys():
                        val2 = 1
                    else:
                        val2 = three_gram[n_gram[0], n_gram[1], n_gram[2]]
                lam = get_lambda([n_gram[0], n_gram[1], n_gram[2]])
                # print(lam, "lam")
                loc_value = kneyser_ney(n_gram[1:])
                # print ("returning ", len(n_gram), value/val2, loc_value, lam)
                return ((value / val2) + (lam * loc_value))
            elif (len(n_gram) == 3):
                count = 0
                sum = 0
                for i in (three_gram.keys()):
                    if(i[2] == n_gram[2]):
                        count += 1
                    if(i[0] == n_gram[0]) and (i[1] == n_gram[1]):
                        sum += three_gram[i]
                value = max(0, count - 0.75)
                sum = count_3
                lam = get_lambda([n_gram[0], n_gram[1]])
                # print(lam, "lam")
                # print value and sum
                # print("value and sum", value, sum)
                loc_value = kneyser_ney(n_gram[1:])
                # print("returning ", len(n_gram), value/sum, loc_value, lam)
                return ((value / sum) + (lam * loc_value))
            elif (len(n_gram) == 2):
                count = 0
                sum = 0
                for i in (two_gram.keys()):
                    if(i[1] == n_gram[1]):
                        count += 1
                    if(i[0] == n_gram[0]):
                        sum += two_gram[i]
                value = max(0, count - 0.75)
                # lam = get_lambda(n_gram[0])
                sum = count_2
                summs = 0
                countts = 0
                for i in (two_gram.keys()):
                    if(i[0] == n_gram[0]):
                        summs += two_gram[i]
                        countts += 1
                        summs = max(summs, 1)
                    
                # print(summs, countts)
                summs = max(summs, 1)
                lam =  ((0.75/summs) * countts)
                # print(lam,"lam")
                loc_value = kneyser_ney(n_gram[1:])
                # print("returning ", len(n_gram), value/sum, loc_value, lam)
                return((value / sum) + (lam *loc_value ))
                    

        # print(four_gram)
        # calculate probability of a sentence using kneser-ney smoothing
        def back_off(n_gram):
            l_p = kneyser_ney(n_gram)
            if l_p == 0:
                return (back_off(n_gram[1:]))
            else:
                return l_p
        def PROB(sentence):
            # split the sentence into a list of words
            sentence = sentence.split()
            # calculate the probability of the sentence
            prob = 1
            for i in range(1,len(sentence)+1):
                # COUNT += 1
                if(i <= 4):
                    # print(sentence[:i])
                    l_p = kneyser_ney(sentence[:i])
                    if l_p == 0:
                        l_p = back_off(sentence[1:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[:i])
                else:
                    # print(sentence[i-4:i])
                    l_p = kneyser_ney(sentence[i-4:i])
                    if(l_p == 0):
                        l_p = back_off(sentence[i-3:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[i-4:i])


        
            return prob

        # def COUNT(sentence):
        #      # split the sentence into a list of words
        #     sentence = sentence.split()
        #     # calculate the probability of the sentence
        #     prob = 1
        #     COUNT = 0
        #     for i in range(1,len(sentence)+1):
        #         COUNT += 1
        #         if(i <= 4):
        #             l_p = kneyser_ney(sentence[:i])
        #             if l_p == 0:
        #                 l_p = back_off(sentence[1:i])
        #             # print (l_p, "-------------------")
        #             prob = prob * l_p
        #             # print(sentence[:i])
        #         else:
        #             l_p = kneyser_ney(sentence[i-4:i])
        #             if(l_p == 0):
        #                 l_p = back_off(sentence[i-3:i])
        #             # print (l_p, "-------------------")
        #             prob = prob * l_p
        #             # print(sentence[i-4:i])


        
        #     return COUNT

        sentence = input("input sentence: ")

        sentence = re.sub(r'\s+', ' ', sentence)
        mention_pattern = re.compile(r'@\w+')
        sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        # remove all punctuation marks except period, question mark, exclamation mark
        sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        sentence = re.sub(r'\bdr\.', 'dr', sentence)
        sentence = re.sub(r'\bmr\.', 'mr', sentence)
        sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        sentence = re.sub(r'\bms\.', 'ms', sentence)
        # remove all numeric characters
        sentence = re.sub(r'\d+', '', sentence)
        # lowercase all letters
        sentence = sentence.lower()
        # remove all underscores
        sentence = re.sub(r'_', '', sentence)


        # print(sentence)
        print(PROB(sentence))



        # print(kneser_ney("i love you a lot"))
        # words = sentence.split()
        # num_words = len(words)
        # print(num_words)

        # print (COUNT(sentence))
        # SUM = 0
        # NUMBER = 0
        # with open('output_training_LM1.txt', 'w') as file:
        #     for line in training_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         try:
        #             probability = (PROB(line))
        #         except:
        #             continue
        #         # probability = (PROB(line))
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         answer = math.pow(1/probability, 1/num_words)
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()


        # SUM = 0
        # NUMBER = 0
        # with open('output_testing_LM1.txt', 'w') as file:
        #     for line in testing_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         try:
        #             probability = (PROB(line))
        #         except:
        #             print(line)
        #             break
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         answer = math.pow(1/probability, 1/num_words)
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()
    else:
        address = path
        text_str = ""
        # Open the file in read mode
        with open(address, 'r') as file:
            # Loop through the lines of the file
            for line in file:
                text_str = text_str + line + " "
        # replace all spaces with a single space
        text_str = re.sub(r'\s+', ' ', text_str)
        # replace all urls with <URL>
        url_pattern = re.compile(r'^https?:\/\/.*[\r\n]*')
        text_str = url_pattern.sub('<URL>', text_str)
        text_str = text_str[938:]
        # replace all mentions with <MENTION>
        mention_pattern = re.compile(r'@\w+')
        text_str = mention_pattern.sub('<MENTIONNN>', text_str)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        text_str = hashtag_pattern.sub('<HASHTAGGG>', text_str)
        # remove all punctuation marks except period, question mark, exclamation mark
        text_str = re.sub(r'[^\w\s.?!]', '', text_str)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        text_str = re.sub(r'\bdr\.', 'dr', text_str)
        text_str = re.sub(r'\bmr\.', 'mr', text_str)
        text_str = re.sub(r'\bmrs\.', 'mrs', text_str)
        text_str = re.sub(r'\bms\.', 'ms', text_str)
        # remove all numeric characters
        text_str = re.sub(r'\d+', '', text_str)
        # lowercase all letters
        text_str = text_str.lower()
        # remove all underscores
        text_str = re.sub(r'_', '', text_str)

        # split text string into a list of sentences
        sentences = re.split(r'[.?!]', text_str)
        training_sentences = sentences
        # print(sentences)
        testing_sentences = random.sample(training_sentences, 1000)
        training_sentences = [sentence for sentence in sentences if sentence not in testing_sentences]
        # split sentences into a list of words
        words = []
        list_of_sentences = list()
        for sentence in training_sentences:
            local_list = list()
            local_list = (sentence.split())
            list_of_sentences.append(local_list)
        # print(list_of_sentences)

        # creating a one-gram
        one_gram = dict()
        for sentence in list_of_sentences:
            for word in sentence:
                if word in one_gram:
                    one_gram[word] += 1
                else:
                    one_gram[word] = 1
        # print(one_gram)

        # creating a two-gram
        two_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 1):
                key = (sentence[i], sentence[i + 1])
                if key in two_gram:
                    two_gram[key] += 1
                else:
                    two_gram[key] = 1
        # print(two_gram)

        # creating a three-gram
        three_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 2):
                key = (sentence[i], sentence[i + 1], sentence[i + 2])
                if key in three_gram:
                    three_gram[key] += 1
                else:
                    three_gram[key] = 1
        # print(three_gram)

        # creating a four-gram
        four_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 3):
                key = (sentence[i], sentence[i + 1], sentence[i + 2], sentence[i + 3])
                if key in four_gram:
                    four_gram[key] += 1
                else:
                    four_gram[key] = 1


        sum_of_all_one_grams = 0
        for i in (one_gram.values()):
            sum_of_all_one_grams += i
        count_3 = len(three_gram.keys())
        count_2 = len(two_gram.keys())
        # print(sum_of_all_one_grams)


        def get_lambda(n_gram):
            n = len(n_gram)
            # print("here len", n, n_gram, type(n_gram))
            if(n == 2):
                sum = 0
                count = 0
                for i in (three_gram.keys()):
                    if(i[0] == n_gram[0]) and (i[1] == n_gram[1]):
                        sum += three_gram[i]
                        count += 1
                sum = max(sum, 1)
                # print(sum, count)
                return ((0.75/sum) * count)
            
            elif(n == 3):
                sum = 0
                count = 0
                for i in (four_gram.keys()):
                    if(i[0] == n_gram[0]) and (i[1] == n_gram[1]) and (i[2] == n_gram[2]):
                        sum += four_gram[i]
                        count += 1
                sum = max(sum, 1)
            
                return ((0.75/sum) * count)


        def kneyser_ney(n_gram):
            # print(n_gram)
            if(len(n_gram) == 1):
                if(n_gram[0] in one_gram.keys()):
                    # print ("returning")
                    return one_gram.get(n_gram[0], 0) / sum_of_all_one_grams
                else:
                    # print ("returning")
                    return 0.75 / sum_of_all_one_grams

            elif (len(n_gram) == 4):
                if (n_gram[0], n_gram[1], n_gram[2], n_gram[3]) in four_gram.keys():
                    val = four_gram[n_gram[0], n_gram[1], n_gram[2], n_gram[3]]
                else:
                    val = 0
                value = max(0, val - 0.75)
                if(value == 0):
                    val2 = 1
                else:
                    if (three_gram[n_gram[0], n_gram[1], n_gram[2]]) not in three_gram.keys():
                        val2 = 1
                    else:
                        val2 = three_gram[n_gram[0], n_gram[1], n_gram[2]]
                lam = get_lambda([n_gram[0], n_gram[1], n_gram[2]])
                # print(lam, "lam")
                loc_value = kneyser_ney(n_gram[1:])
                # print ("returning ", len(n_gram), value/val2, loc_value, lam)
                return ((value / val2) + (lam * loc_value))
            elif (len(n_gram) == 3):
                count = 0
                sum = 0
                for i in (three_gram.keys()):
                    if(i[2] == n_gram[2]):
                        count += 1
                    if(i[0] == n_gram[0]) and (i[1] == n_gram[1]):
                        sum += three_gram[i]
                value = max(0, count - 0.75)
                sum = count_3
                lam = get_lambda([n_gram[0], n_gram[1]])
                # print(lam, "lam")
                # print value and sum
                # print("value and sum", value, sum)
                loc_value = kneyser_ney(n_gram[1:])
                # print("returning ", len(n_gram), value/sum, loc_value, lam)
                return ((value / sum) + (lam * loc_value))
            elif (len(n_gram) == 2):
                count = 0
                sum = 0
                for i in (two_gram.keys()):
                    if(i[1] == n_gram[1]):
                        count += 1
                    if(i[0] == n_gram[0]):
                        sum += two_gram[i]
                value = max(0, count - 0.75)
                # lam = get_lambda(n_gram[0])
                sum = count_2
                summs = 0
                countts = 0
                for i in (two_gram.keys()):
                    if(i[0] == n_gram[0]):
                        summs += two_gram[i]
                        countts += 1
                        summs = max(summs, 1)
                    
                # print(summs, countts)
                summs = max(summs, 1)
                lam =  ((0.75/summs) * countts)
                # print(lam,"lam")
                loc_value = kneyser_ney(n_gram[1:])
                # print("returning ", len(n_gram), value/sum, loc_value, lam)
                return((value / sum) + (lam *loc_value ))
                    

        # print(four_gram)
        # calculate probability of a sentence using kneser-ney smoothing
        def back_off(n_gram):
            l_p = kneyser_ney(n_gram)
            if l_p == 0:
                return (back_off(n_gram[1:]))
            else:
                return l_p
        def PROB(sentence):
            # split the sentence into a list of words
            sentence = sentence.split()
            # calculate the probability of the sentence
            prob = 1
            for i in range(1,len(sentence)+1):
                # COUNT += 1
                if(i <= 4):
                    l_p = kneyser_ney(sentence[:i])
                    if l_p == 0:
                        l_p = back_off(sentence[1:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[:i])
                else:
                    l_p = kneyser_ney(sentence[i-4:i])
                    if(l_p == 0):
                        l_p = back_off(sentence[i-3:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[i-4:i])


        
            return prob

        # def COUNT(sentence):
        #      # split the sentence into a list of words
        #     sentence = sentence.split()
        #     # calculate the probability of the sentence
        #     prob = 1
        #     COUNT = 0
        #     for i in range(1,len(sentence)+1):
        #         COUNT += 1
        #         if(i <= 4):
        #             l_p = kneyser_ney(sentence[:i])
        #             if l_p == 0:
        #                 l_p = back_off(sentence[1:i])
        #             # print (l_p, "-------------------")
        #             prob = prob * l_p
        #             # print(sentence[:i])
        #         else:
        #             l_p = kneyser_ney(sentence[i-4:i])
        #             if(l_p == 0):
        #                 l_p = back_off(sentence[i-3:i])
        #             # print (l_p, "-------------------")
        #             prob = prob * l_p
        #             # print(sentence[i-4:i])


        
        #     return COUNT



        # print(kneser_ney("i love you a lot"))
        sentence = input("input sentence: ")

        sentence = re.sub(r'\s+', ' ', sentence)
        mention_pattern = re.compile(r'@\w+')
        sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        # remove all punctuation marks except period, question mark, exclamation mark
        sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        sentence = re.sub(r'\bdr\.', 'dr', sentence)
        sentence = re.sub(r'\bmr\.', 'mr', sentence)
        sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        sentence = re.sub(r'\bms\.', 'ms', sentence)
        # remove all numeric characters
        sentence = re.sub(r'\d+', '', sentence)
        # lowercase all letters
        sentence = sentence.lower()
        # remove all underscores
        sentence = re.sub(r'_', '', sentence)


        # print(sentence)
        print(PROB(sentence))
        # words = sentence.split()
        # num_words = len(words)
        # print(num_words)

        # print (COUNT(sentence))
        # SUM = 0
        # NUMBER = 0
        # with open('output_training_LM2.txt', 'w') as file:
        #     for line in training_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         try:
        #             probability = (PROB(line))
        #         except:
        #             continue
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         if(probability == 0):
        #             probability = 0.0000000000000001
        #         answer = math.pow(1/probability, 1/num_words)
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()


        # SUM = 0
        # NUMBER = 0
        # with open('output_testing_LM2.txt', 'w') as file:
        #     for line in testing_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         try:
        #             probability = (PROB(line))
        #         except:
        #             continue
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         if(probability == 0):
        #             probability = 0.0000000000000001
        #         answer = math.pow(1/probability, 1/num_words)
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     print(SUM)
        #     print(NUMBER)
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()
else:
    if(path == 'Pride.txt'):
# to make a tokenizer using regex

        text_str = ""
        # Open the file in read mode
        with open('Pride.txt', 'r') as file:
            # Loop through the lines of the file
            for line in file:
                text_str = text_str + line + " "
        # replace all spaces with a single space
        text_str = re.sub(r'\s+', ' ', text_str)
        # replace all urls with <URL>
        url_pattern = re.compile(r'^https?:\/\/.*[\r\n]*')
        text_str = url_pattern.sub('<URL>', text_str)
        text_str = text_str[1713:-18524]
        # replace all mentions with <MENTION>
        mention_pattern = re.compile(r'@\w+')
        text_str = mention_pattern.sub('<MENTIONNN>', text_str)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        text_str = hashtag_pattern.sub('<HASHTAGGG>', text_str)
        # remove all punctuation marks except period, question mark, exclamation mark
        text_str = re.sub(r'[^\w\s.?!]', '', text_str)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        text_str = re.sub(r'\bdr\.', 'dr', text_str)
        text_str = re.sub(r'\bmr\.', 'mr', text_str)
        text_str = re.sub(r'\bmrs\.', 'mrs', text_str)
        text_str = re.sub(r'\bms\.', 'ms', text_str)
        # remove all numeric characters
        text_str = re.sub(r'\d+', '', text_str)
        # lowercase all letters
        text_str = text_str.lower()
        # remove all underscores
        text_str = re.sub(r'_', '', text_str)

        # split text string into a list of sentences
        sentences = re.split(r'[.?!]', text_str)
        training_sentences = sentences
        # print(sentences)
        testing_sentences = random.sample(training_sentences, 1000)
        training_sentences = [
            sentence for sentence in sentences if sentence not in testing_sentences]
        # split sentences into a list of words
        words = []
        list_of_sentences = list()
        for sentence in training_sentences:
            local_list = list()
            local_list = (sentence.split())
            list_of_sentences.append(local_list)
        # print(list_of_sentences)

        # creating a one-gram
        one_gram = dict()
        for sentence in list_of_sentences:
            for word in sentence:
                if word in one_gram:
                    one_gram[word] += 1
                else:
                    one_gram[word] = 1
        # print(one_gram)

        # creating a two-gram
        two_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 1):
                key = (sentence[i], sentence[i + 1])
                if key in two_gram:
                    two_gram[key] += 1
                else:
                    two_gram[key] = 1
        # print(two_gram)

        # creating a three-gram
        three_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 2):
                key = (sentence[i], sentence[i + 1], sentence[i + 2])
                if key in three_gram:
                    three_gram[key] += 1
                else:
                    three_gram[key] = 1
        # print(three_gram)

        # creating a four-gram
        four_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 3):
                key = (sentence[i], sentence[i + 1], sentence[i + 2], sentence[i + 3])
                if key in four_gram:
                    four_gram[key] += 1
                else:
                    four_gram[key] = 1


        sum_of_all_one_grams = 0
        for i in (one_gram.values()):
            sum_of_all_one_grams += i
        count_3 = len(three_gram.keys())
        count_2 = len(two_gram.keys())
        count_1 = len(one_gram.keys())
        # print(sum_of_all_one_grams)


        sentence = input("input sentence: ")

        sentence = re.sub(r'\s+', ' ', sentence)
        mention_pattern = re.compile(r'@\w+')
        sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        # remove all punctuation marks except period, question mark, exclamation mark
        sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        sentence = re.sub(r'\bdr\.', 'dr', sentence)
        sentence = re.sub(r'\bmr\.', 'mr', sentence)
        sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        sentence = re.sub(r'\bms\.', 'ms', sentence)
        # remove all numeric characters
        sentence = re.sub(r'\d+', '', sentence)
        # lowercase all letters
        sentence = sentence.lower()
        # remove all underscores
        sentence = re.sub(r'_', '', sentence)


        def get_lambda(n_gram):
            numb = 1
            n = len(n_gram)
            sum = 0
            num = 0
            if(n == 3):
                for i in four_gram.keys():
                    if(n_gram[0] == i[0]) and (n_gram[1] == i[1]) and (n_gram[2] == i[2]):
                        sum += four_gram[i]
                        num += 1
                if(num == 0):
                    sum = 1
                return(num/(sum+num))
            elif(n == 2):
                for i in three_gram.keys():
                    if(n_gram[0] == i[0]) and (n_gram[1] == i[1]):
                        sum += three_gram[i]
                        num += 1
                if(num == 0):
                    sum = 1
                return(num/(sum+num))
            elif(n == 1):
                for i in two_gram.keys():
                    if(n_gram[0] == i[0]):
                        sum += two_gram[i]
                        num += 1
                if(num == 0):
                    sum = 1
                return(num/(sum+num))
        turing_estimate = 0
        for value in one_gram.values():
            if(value == 1):
                turing_estimate += 1

        def witten_bell(n_gram):
            if(len(n_gram) == 0):
                return (1)
            else:
                n = len(n_gram)
                lam = get_lambda(n_gram[:-1])
                if(n == 4):
                    val = 0
                    count = 0
                    if n_gram in four_gram:
                        val = four_gram[n_gram[0], n_gram[1], n_gram[2], n_gram[3]]
                    else:
                        val = 0
                    if n_gram[:-1] in three_gram:
                        count = three_gram[n_gram[0], n_gram[1], n_gram[2]]
                    else:
                        count = 1
                    pml = val/count
                    return ((lam * pml) + ((1 - lam) * witten_bell(n_gram[1:])))

                elif(n == 3):
                    val = 0
                    count = 0
                    if n_gram in three_gram:
                        val = three_gram[n_gram[0], n_gram[1], n_gram[2]]
                    else:
                        val = 0
                    if n_gram[:-1] in two_gram:
                        count = two_gram[n_gram[0], n_gram[1]]
                    else:
                        count = 1
                    pml = val/count
                    return ((lam * pml) + ((1 - lam) * witten_bell(n_gram[1:])))

                elif(n == 2):
                    val = 0
                    count = 0
                    if n_gram in two_gram:
                        val = two_gram[n_gram[0], n_gram[1]]
                    else:
                        val = 0
                    if n_gram[:-1] in one_gram:
                        count = one_gram[n_gram[0]]
                    else:
                        count = 1
                    pml = val/count
                    return ((lam * pml) + ((1 - lam) * witten_bell(n_gram[1:])))

                elif(n == 1):
                    val = 0
                    count = sum_of_all_one_grams
                    # print("---->", n_gram, type(n_gram), type(n_gram[0]))
                    if n_gram in one_gram.keys():
                        # print("in one gram: ", n_gram)
                        val = one_gram[n_gram]
                    else:
                        val = turing_estimate 
                    return(val/count)

            # print(sentence)


        def back_off(n_gram):
            l_p = witten_bell(n_gram)
            if l_p == 0:
                return (back_off(n_gram[1:]))
            else:
                return l_p


        def PROB(sentence):
            words = sentence.split()
            num_words = len(words)
            # print("entered prob", num_words, words)
            prob = 1
            for i in range(num_words+1):
                # print("i = ", i)
                if(i <= 4):
                    # print(sentence[:i])
                    l_p = witten_bell(sentence[:i])
                    if l_p == 0:
                        l_p = back_off(sentence[1:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[:i])
                else:
                    # print(sentence[i-4:i])
                    l_p = witten_bell(sentence[i-4:i])
                    if(l_p == 0):
                        l_p = back_off(sentence[i-3:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[i-4:i])
            return prob


        print(PROB(sentence))


        # SUM = 0
        # NUMBER = 0
        # with open('output_training_LM3.txt', 'w') as file:
        #     for line in training_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         probability = (PROB(line))
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         try:
        #             answer = math.pow(1/probability, 1/num_words)
        #         except:
        #             continue
        #         if(math.isinf(answer) == 1):
        #             continue
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()


        # SUM = 0
        # NUMBER = 0
        # with open('output_testing_LM3.txt', 'w') as file:
        #     for line in testing_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         try:
        #             probability = (PROB(line))
        #         except:
        #             print(line)
        #             break
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         try:
        #             answer = math.pow(1/probability, 1/num_words)
        #         except:
        #             continue
        #         if(math.isinf(answer) == 1):
        #             continue
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()
    else:
        # to make a tokenizer using regex

        text_str = ""
        # Open the file in read mode
        with open('Ulysses.txt', 'r') as file:
            # Loop through the lines of the file
            for line in file:
                text_str = text_str + line + " "
        # replace all spaces with a single space
        text_str = re.sub(r'\s+', ' ', text_str)
        # replace all urls with <URL>
        url_pattern = re.compile(r'^https?:\/\/.*[\r\n]*')
        text_str = url_pattern.sub('<URL>', text_str)
        text_str = text_str[938:]
        # replace all mentions with <MENTION>
        mention_pattern = re.compile(r'@\w+')
        text_str = mention_pattern.sub('<MENTIONNN>', text_str)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        text_str = hashtag_pattern.sub('<HASHTAGGG>', text_str)
        # remove all punctuation marks except period, question mark, exclamation mark
        text_str = re.sub(r'[^\w\s.?!]', '', text_str)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        text_str = re.sub(r'\bdr\.', 'dr', text_str)
        text_str = re.sub(r'\bmr\.', 'mr', text_str)
        text_str = re.sub(r'\bmrs\.', 'mrs', text_str)
        text_str = re.sub(r'\bms\.', 'ms', text_str)
        # remove all numeric characters
        text_str = re.sub(r'\d+', '', text_str)
        # lowercase all letters
        text_str = text_str.lower()
        # remove all underscores
        text_str = re.sub(r'_', '', text_str)

        # split text string into a list of sentences
        sentences = re.split(r'[.?!]', text_str)
        training_sentences = sentences
        # print(sentences)
        testing_sentences = random.sample(training_sentences, 1000)
        training_sentences = [
            sentence for sentence in sentences if sentence not in testing_sentences]
        # split sentences into a list of words
        words = []
        list_of_sentences = list()
        for sentence in training_sentences:
            local_list = list()
            local_list = (sentence.split())
            list_of_sentences.append(local_list)
        # print(list_of_sentences)

        # creating a one-gram
        one_gram = dict()
        for sentence in list_of_sentences:
            for word in sentence:
                if word in one_gram:
                    one_gram[word] += 1
                else:
                    one_gram[word] = 1
        # print(one_gram)

        # creating a two-gram
        two_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 1):
                key = (sentence[i], sentence[i + 1])
                if key in two_gram:
                    two_gram[key] += 1
                else:
                    two_gram[key] = 1
        # print(two_gram)

        # creating a three-gram
        three_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 2):
                key = (sentence[i], sentence[i + 1], sentence[i + 2])
                if key in three_gram:
                    three_gram[key] += 1
                else:
                    three_gram[key] = 1
        # print(three_gram)

        # creating a four-gram
        four_gram = dict()
        for sentence in list_of_sentences:
            for i in range(len(sentence) - 3):
                key = (sentence[i], sentence[i + 1], sentence[i + 2], sentence[i + 3])
                if key in four_gram:
                    four_gram[key] += 1
                else:
                    four_gram[key] = 1


        sum_of_all_one_grams = 0
        for i in (one_gram.values()):
            sum_of_all_one_grams += i
        count_3 = len(three_gram.keys())
        count_2 = len(two_gram.keys())
        count_1 = len(one_gram.keys())
        # print(sum_of_all_one_grams)


        sentence = input("input sentence: ")

        sentence = re.sub(r'\s+', ' ', sentence)
        mention_pattern = re.compile(r'@\w+')
        sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        # replace all hashtags with <HASHTAG>
        hashtag_pattern = re.compile(r'#\w+')
        sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        # remove all punctuation marks except period, question mark, exclamation mark
        sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        # replace dr. mr. mrs. ms. with dr mr mrs ms
        sentence = re.sub(r'\bdr\.', 'dr', sentence)
        sentence = re.sub(r'\bmr\.', 'mr', sentence)
        sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        sentence = re.sub(r'\bms\.', 'ms', sentence)
        # remove all numeric characters
        sentence = re.sub(r'\d+', '', sentence)
        # lowercase all letters
        sentence = sentence.lower()
        # remove all underscores
        sentence = re.sub(r'_', '', sentence)


        def get_lambda(n_gram):
            numb = 1
            n = len(n_gram)
            sum = 0
            num = 0
            if(n == 3):
                for i in four_gram.keys():
                    if(n_gram[0] == i[0]) and (n_gram[1] == i[1]) and (n_gram[2] == i[2]):
                        sum += four_gram[i]
                        num += 1
                if(num == 0):
                    sum = 1
                return(num/(sum+num))
            elif(n == 2):
                for i in three_gram.keys():
                    if(n_gram[0] == i[0]) and (n_gram[1] == i[1]):
                        sum += three_gram[i]
                        num += 1
                if(num == 0):
                    sum = 1
                return(num/(sum+num))
            elif(n == 1):
                for i in two_gram.keys():
                    if(n_gram[0] == i[0]):
                        sum += two_gram[i]
                        num += 1
                if(num == 0):
                    sum = 1
                return(num/(sum+num))
        turing_estimate = 0
        for value in one_gram.values():
            if(value == 1):
                turing_estimate += 1

        def witten_bell(n_gram):
            if(len(n_gram) == 0):
                return (1)
            else:
                n = len(n_gram)
                lam = get_lambda(n_gram[:-1])
                if(n == 4):
                    val = 0
                    count = 0
                    if n_gram in four_gram:
                        val = four_gram[n_gram[0], n_gram[1], n_gram[2], n_gram[3]]
                    else:
                        val = 0
                    if n_gram[:-1] in three_gram:
                        count = three_gram[n_gram[0], n_gram[1], n_gram[2]]
                    else:
                        count = 1
                    pml = val/count
                    return ((lam * pml) + ((1 - lam) * witten_bell(n_gram[1:])))

                elif(n == 3):
                    val = 0
                    count = 0
                    if n_gram in three_gram:
                        val = three_gram[n_gram[0], n_gram[1], n_gram[2]]
                    else:
                        val = 0
                    if n_gram[:-1] in two_gram:
                        count = two_gram[n_gram[0], n_gram[1]]
                    else:
                        count = 1
                    pml = val/count
                    return ((lam * pml) + ((1 - lam) * witten_bell(n_gram[1:])))

                elif(n == 2):
                    val = 0
                    count = 0
                    if n_gram in two_gram:
                        val = two_gram[n_gram[0], n_gram[1]]
                    else:
                        val = 0
                    if n_gram[:-1] in one_gram:
                        count = one_gram[n_gram[0]]
                    else:
                        count = 1
                    pml = val/count
                    return ((lam * pml) + ((1 - lam) * witten_bell(n_gram[1:])))

                elif(n == 1):
                    val = 0
                    count = sum_of_all_one_grams
                    # print("---->", n_gram, type(n_gram), type(n_gram[0]))
                    if n_gram in one_gram.keys():
                        # print("in one gram: ", n_gram)
                        val = one_gram[n_gram]
                    else:
                        val = turing_estimate 
                    return(val/count)

            # print(sentence)


        def back_off(n_gram):
            l_p = witten_bell(n_gram)
            if l_p == 0:
                return (back_off(n_gram[1:]))
            else:
                return l_p


        def PROB(sentence):
            words = sentence.split()
            num_words = len(words)
            # print("entered prob", num_words, words)
            prob = 1
            for i in range(num_words+1):
                # print("i = ", i)
                if(i <= 4):
                    # print(sentence[:i])
                    l_p = witten_bell(sentence[:i])
                    if l_p == 0:
                        l_p = back_off(sentence[1:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[:i])
                else:
                    # print(sentence[i-4:i])
                    l_p = witten_bell(sentence[i-4:i])
                    if(l_p == 0):
                        l_p = back_off(sentence[i-3:i])
                    # print (l_p, "-------------------")
                    prob = prob * l_p
                    # print(sentence[i-4:i])
            return prob


        print(PROB(sentence))


        # SUM = 0
        # NUMBER = 0
        # with open('output_training_LM4.txt', 'w') as file:
        #     for line in training_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         probability = (PROB(line))
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         try:
        #             answer = math.pow(1/probability, 1/num_words)
        #         except:
        #             continue
        #         if(math.isinf(answer) == 1):
        #             continue
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " - " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()


        # SUM = 0
        # NUMBER = 0
        # with open('output_testing_LM4.txt', 'w') as file:
        #     for line in testing_sentences:
        #         sentence = line
        #         sentence = re.sub(r'\s+', ' ', sentence)
        #         mention_pattern = re.compile(r'@\w+')
        #         sentence = mention_pattern.sub('<MENTIONNN>', sentence)
        #         # replace all hashtags with <HASHTAG>
        #         hashtag_pattern = re.compile(r'#\w+')
        #         sentence = hashtag_pattern.sub('<HASHTAGGG>', sentence)
        #         # remove all punctuation marks except period, question mark, exclamation mark
        #         sentence = re.sub(r'[^\w\s.?!]', '', sentence)
        #         # replace dr. mr. mrs. ms. with dr mr mrs ms
        #         sentence = re.sub(r'\bdr\.', 'dr', sentence)
        #         sentence = re.sub(r'\bmr\.', 'mr', sentence)
        #         sentence = re.sub(r'\bmrs\.', 'mrs', sentence)
        #         sentence = re.sub(r'\bms\.', 'ms', sentence)
        #         # remove all numeric characters
        #         sentence = re.sub(r'\d+', '', sentence)
        #         # lowercase all letters
        #         sentence = sentence.lower()
        #         # remove all underscores
        #         sentence = re.sub(r'_', '', sentence)
        #         line = sentence
        #         try:
        #             answer = math.pow(1/probability, 1/num_words)
        #         except:
        #             continue
        #         if(math.isinf(answer) == 1):
        #             continue
        #         words = line.split()
        #         num_words = len(words)
        #         if(num_words == 0):
        #             num_words = 1
        #         answer = math.pow(1/probability, 1/num_words)
        #         NUMBER += 1
        #         SUM += answer
        #         file.write(str(line + " " + str(answer) + "\n"))
        #     avg = SUM/NUMBER
        #     print(avg)
        #     file.write("Average perplexity: " + str(avg))
        #     file.close()
