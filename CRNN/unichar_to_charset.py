UNICHAR_FILE = 'CRNN/charset/myanmar.unicharset'
TXT_FILE = 'CRNN/charset/myanmar.txt'

with open(UNICHAR_FILE, 'r') as f:
    with open(TXT_FILE, 'w+') as new_f:
        lines = f.readlines()
        for line in lines:
            print("word to write ", line[0])
            new_f.write(str(line[0])+'\n')
