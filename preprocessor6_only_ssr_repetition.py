# coding: utf-8

__author__ = 'linlin'
import os
import logging
import re
import pdb

logger = logging.getLogger(__name__)
################################################################
root_dir = '/home/linlin/time/0903_classify_false_start/1003_raw_features/'
separator = '\t\t'
################################################################


def MakeNewFolderVersionHigher(data_directory, dir_name):
    ## 在选定的文件夹里生成更高版本号的文件夹 data_directory - can be relative directory
    ## dir_name - the new folder name you want to creat
    abs_data_directory = os.path.abspath(os.path.dirname(data_directory))
    version_number = 1
    dirs = os.listdir(abs_data_directory)
    for  dir in dirs:
        if dir_name in dir:
            version_str = re.findall(r'Dir_\d+',dir)
            number_str =''.join((version_str[-1])[4:])
            if True == number_str.isdigit():
                number= int (number_str)
                if number>version_number:
                    version_number = number
    new_folder_name = dir_name + "_%d" %(version_number+1)
    folderFullPath = os.path.join(abs_data_directory,new_folder_name )
    os.makedirs(folderFullPath)
    return folderFullPath

#########################################################
output_root_dir = MakeNewFolderVersionHigher(root_dir, 'processDir' )
data_dir = root_dir + 'data1'
code_dir = root_dir + 'src/'
##############################################################

def DirProcessing(source_path, dest_path):
    path = source_path

    for root, dirs, files in os.walk(path):
        for filespath in files:
            abs_file_path = os.path.join(root, filespath)
            logger.debug("Visited one file!")
            Standardize(abs_file_path, dest_path, ' ')



def DirProcessingForSSR(source_path, dest_path):
    path = source_path

    for root, dirs, files in os.walk(path):
        for filespath in files:
            abs_file_path = os.path.join(root, filespath)
            logger.debug("Visited one file!")
            GetSsrFeature(abs_file_path, dest_path, '\t')




def GetAttributes(source_path, dest_path):
################################################################
    script_file = code_dir + 'chunker6_only_ssr_repetition.py'
################################################################
    path = source_path

    for root, dirs, files in os.walk(path):
        for filespath in files:
            abs_file_path = os.path.join(root, filespath)
            logger.debug("Visited one file!")
            crf_path = dest_path + '/' + os.path.basename(abs_file_path) + '.crfsuite'
            os.system('cat ' + abs_file_path +'  | python ' + script_file + " > " + crf_path )


def RunClassifier(source_path, dest_path):
    path = source_path

    for root, dirs, files in os.walk(path):
        for filespath in files:
            if 'tr.txt' in filespath:
                train_path = os.path.join(root, filespath)
            elif 'te.txt' in filespath:
                test_path = os.path.join(root, filespath)
    #pdb.set_trace()
    result_path = dest_path + '/' +  'result.txt'
    os.system('crfsuite learn -e2 ' + train_path + " " + test_path +  " > " + result_path )

def FindNeighborTokenSubscript(first_token_list, current_pos , up_or_down ):
    pos = current_pos
    ind = up_or_down
    li = first_token_list
    if ind == 1:
        i = 1
        while len(li[pos+i]) < 1:
            i += 1
        return pos+i

    if ind == -1:
        i = 1
        while len(li[pos-i]) < 1:
            i += 1
        return pos-i



def Standardize(path, dest_dir,  sep):
    output_path = dest_dir+ '/' + os.path.basename(path) + '.standard'
    output_file_obj = open(output_path,'w')

    file_obj = open(path)
    line_list = file_obj.readlines()

    token_list = []
    for j in range(len(line_list)):
        word_list = line_list[j].split()
        if len(word_list) < 2:
            token_list.append('')
        else:
            token_list.append(word_list[0])


    repetition_vec_list = []
    for i in range(len(line_list)):
        if len(token_list[i]) == 0:
            repetition_vec_list.append('')
        else:
            if i < 4  or i > len(line_list)- 5:
                repetition_vec_list.append(['diff', 'diff','diff', 'diff'])
            else:
                previous_subscript = FindNeighborTokenSubscript(token_list, i, -1)
                prev_prev_subscript = FindNeighborTokenSubscript(token_list, previous_subscript, -1)
                next_subscript = FindNeighborTokenSubscript(token_list, i, 1)
                next_next_subscript = FindNeighborTokenSubscript(token_list, next_subscript, 1)
                prev_prev_label = 'same' if (token_list[i] == token_list[prev_prev_subscript]) else "diff"
                prev_label = 'same' if (token_list[i] == token_list[previous_subscript]) else "diff"
                next_label = 'same' if (token_list[i] == token_list[next_subscript]) else "diff"
                next_next_subscript = 'same' if (token_list[i] == token_list[next_next_subscript]) else "diff"
                repetition_vec_list.append([prev_prev_label, prev_label, next_label, next_next_subscript])


    for k in range(len(line_list)):
        line = line_list[k]
        if len(line)<13:
            label = ''
        else:
            word_list = line.split()

            if 'filler' in word_list[4]:
                label = 'filler'
            elif 'repeat' in word_list[4] or 'nsert' in word_list[4]:
                label = 'repeat'
            elif 'restart' in word_list[4] or 'extraneou' in word_list[4]:
                label = 'false_start'
            elif 'elete' in word_list[4]:
                label = 'other'
            else:
                label = 'OK'

            if '-' in word_list[0]:
                patial = 'patial'
            else:
                patial = 'nonpatial'

            label = label
            token = word_list[0]
            pos = word_list[1]
            word = word_list[2]
            sem = word_list[3]
            patial = patial
            #pdb.set_trace()
            pp = repetition_vec_list[k][0]
            p = repetition_vec_list[k][1]
            n = repetition_vec_list[k][2]
            nn = repetition_vec_list[k][3]

        #pdb.set_trace()
        if len(line)<13:
            line_format = ''
        else:
            line_format = (
                "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s"
                %(label, sep, token,sep,pos, sep,word,sep,sem, sep, patial, sep,
                  pp, sep, p, sep, n,sep, nn))

        output_file_obj.write(line_format)
        output_file_obj.write('\n')

    output_file_obj.close()
    file_obj.close()



def GetSsrFeature(path, dest_dir,  sep):
    output_path = dest_dir+ '/' + os.path.basename(path) + '.noSpace'
    output_file_obj = open(output_path,'w')

    file_obj = open(path)

    for line in file_obj:
        if len(line)<3:
            newLine = ''
        else:
            word_list = line[54:].split()
            newLine = '_'.join(word_list)

        token = line[:15].strip()
        pos = line[15:25].strip()
        word = line[25:40].strip()
        sem = line[40:54].strip()
        label = newLine

        if len(line)<3:
            line_format = ''
        else:
            line_format = "%s%s%s%s%s%s%s%s%s%s" %(token,sep,pos,sep,word,sep,sem, sep, label, sep)

        output_file_obj.write(line_format)
        output_file_obj.write('\n')

    output_file_obj.close()
    file_obj.close()


if __name__ == '__main__':


    logFile = output_root_dir + "/logFile.txt"
    logging.basicConfig(filename=logFile, level = logging.DEBUG)

    os.makedirs(output_root_dir + "/standardStep1")
    dest_dir = output_root_dir + "/standardStep1"
    DirProcessing(data_dir, dest_dir)

    # os.makedirs(output_root_dir + "/standardStep2") #
    # dest_dir = output_root_dir + "/standardStep2"
    # DirProcessing(data_dir, dest_dir) #

    os.makedirs(output_root_dir + "/attributesStep3")
    attr_dir = output_root_dir + "/attributesStep3"
    GetAttributes(dest_dir, attr_dir)

    os.makedirs(output_root_dir + "/classificationStep4")
    result_dir = output_root_dir + "/classificationStep4"
    RunClassifier( attr_dir, result_dir)
