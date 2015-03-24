import preprocessor2
import pdb

if __name__ == '__main__':


    # logFile = parDir + "/logFile.txt"
    # logging.basicConfig(filename=logFile, level = logging.DEBUG)
    #pdb.set_trace()
    path = preprocessor2.MakeNewFolderVersionHigher(".", 'linlinTest')
    print path
