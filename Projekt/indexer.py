import codecs

list_of_chars = [' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z', 'y', 'z', 'ä', 'å', 'ö']
combinations = []

for first_char in list_of_chars:
    for second_char in list_of_chars:
        combinations.append(first_char + second_char)

offset = 0
current_combination_index = 0
first = True
with codecs.open('bigrams_clean.txt','rb',encoding='utf8') as file_read:
    line = file_read.readline()
    with codecs.open('index.txt','w',encoding='utf8') as file_write:
        for combination in combinations:
            if line[:2] == combination:
                file_write.write(combination + ' ' + str(offset) + '\n')
                while line[:2] == combination:
                    offset += len(line.encode('utf-8'))
                    line = file_read.readline()
            else:
                file_write.write(combination + ' -1\n')
