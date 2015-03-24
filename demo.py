__author__ = 'linlin'
import os
import logging
import re
import random

parDir = os.path.dirname(os.getcwd())
# curDir = os.getcwd()
logger = logging.getLogger(__name__)
separator = ' '
text = []

RED = '\033[0;31;40m'
GREEN = '\033[0;32;40m'
YELLOW = '\033[0;33;40m'
BLUE = '\033[0;34;40m'
NORM = '\033[0m'

def GetDataStructure():
    demo_path = parDir + '/data/0112nonCopyAsOKSeparator/demo.txt'
    demo_f_obj = open(demo_path)
    # text = [[['', ], ], ]
    # word = []
    sent = []

    for line in demo_f_obj:
        if len(line.strip()) < 2:
            if len(sent) > 0:
                text.append(sent)
            else:
                logger.debug("more than one empty line were encounted!")
            sent = []
        else:
            list = re.findall(r'\S+\s', line)
            if len(list) != 6:
                list = list + ['^'] * (6 - len(list))
                logger.debug("Number of fields is not equal to 6, it's %d", len(list))
            word = [list[0].strip(), list[1].strip(),list[2].strip(),list[3].strip(),list[4].strip(),list[5].strip()]
            sent.append(word)


def Demo(id_sent):
    oriTokens = ''
    poses = ''
    sems = ''
    predicWords = ''
    goldWords = ''
    reconstrWords = ''
    for word in text[id_sent]:
        oriTokens = oriTokens + word[0] + '\t'
        poses += word[1] + '\t'
        sems  += word[3] + '\t'
        if 'OK' in word[5]:
            predicWord = word[0]
        if 'fille' in word[5]:
            predicWord = GREEN + word[0] + NORM
        if 'repe' in word[5]:
            predicWord = YELLOW + word[0] + NORM
        if 'false' in word[5]:
            predicWord = RED + word[0] + NORM
        if 'OK' in word[4]:
            goldWord = word[0]
        if 'fille' in word[4]:
            goldWord = GREEN + word[0] + NORM
        if 'repe' in word[4]:
            goldWord = YELLOW + word[0] + NORM
        if 'false' in word[4]:
            goldWord = RED + word[0] + NORM
        predicWords += predicWord + '\t'
        goldWords += goldWord + '\t'
        if not ('^' in word[2]):
            reconstrWords += word[2] + '\t'

    # print(oriTokens.strip()+'\n')
    # print(poses.strip()+'\n')
    # print(sems.strip()+'\n')
    # print(predicWords.strip()+'\n')
    # print(goldWords.strip()+'\n')
    # print(reconstrWords.strip()+'\n')

    print(oriTokens.strip()+'\n')
    print(poses.strip())
    print(sems.strip() + '\n')
    print(predicWords.strip()+'\n')
    print(goldWords.strip()+ '\n')
    print(reconstrWords.strip()+'\n')



if __name__ == '__main__':


    logFile = parDir + "/data/0112nonCopyAsOKSeparator/demoLog.txt"
    logging.basicConfig(filename=logFile, level = logging.DEBUG)

    GetDataStructure()

    running = True
    currentID = 0
    while running:
        choice = input("Input: q -exit; r - random sentence; an interger - that sentence; Only ENTER - next sentence \n")
        print('\n')

        if 'q' == choice:
            running = False
        elif 'r' == choice:
            k = random.randint(1, len(text))
            while True:
                isEmpty = True
                for word in text[k]:
                    if '^' in word[3]:
                        isEmpty = True
                    else:
                        isEmpty = False
                        break
                if isEmpty == False:
                    currentID = k
                    Demo(currentID)
                    break
                else:
                    k = k+1

        elif len(choice.strip()) <1:
            currentID = currentID + 1
            Demo(currentID)
        elif choice.isdigit() == True:
            if currentID > len(text):
                print ("There are not that many sentences!")
            else:
                currentID = int(choice)
                Demo(currentID)
        else:
            print("Input invalid, please try another!")

