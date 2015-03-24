__author__ = 'linlin'
import os
import logging
import re

parDir = os.path.dirname(os.getcwd())
# curDir = os.getcwd()
logger = logging.getLogger(__name__)
separator = ' '


def MergePrediction():
    prediction_path = parDir + '/data/0112nonCopyAsOKSeparator/result.txt'
    preprocessed_path = parDir + '/data/0112nonCopyAsOKSeparator/te.txt.preprocess'
    demo_path = parDir + '/data/0112nonCopyAsOKSeparator/demo.txt'

    predic_f_obj = open(prediction_path)
    preproc_f_obj = open(preprocessed_path)
    demo_f_obj = open(demo_path, 'w')

    sentPredic = predic_f_obj.readlines()

    id_sent = 0
    for line in preproc_f_obj:
        match_obj = re.search('\s\w+$', sentPredic[id_sent])
        if None == match_obj:
            tagPredic = ''
        else:
            tagPredic = separator + match_obj.group().strip()
        id_sent += 1
        newLine = line.strip() +  tagPredic
        demo_f_obj.write(newLine)
        demo_f_obj.write('\n')

    demo_f_obj.close()
    preproc_f_obj.close()
    predic_f_obj.close()


if __name__ == '__main__':


    logFile = parDir + "/data/0112nonCopyAsOKSeparator/MergePredictionLog.txt"
    logging.basicConfig(filename=logFile, level = logging.DEBUG)

    MergePrediction()
