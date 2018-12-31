import os
import json
import argparse

ROW_COUNT_PER_FILE = 500000
def validateRecord(row):
    if len(row) != 10:
        print ("Bad row = " + str(row))
        return 1
    else:
        return 0
    
def createJSONRecord(row):
        return {
           "GenomicCoordinate" : row[0],
           "Chrom" : row[1],
           "Pos" : row[2],
           "Ref" : row[3],
           "alt" : row[4],
           "aaref" : row[5],
           "aaalt" : row[6],
           "GeneSymbol" : row[7],
           "Ensembl_transcriptid" : row[8],
           "MVP_Score" : row[9],
            }


def writeRecordToFile(result, fileDescriptor):
    json_data = json.dumps(result, indent=2, skipkeys=True, sort_keys=False)
    fileDescriptor.write(json_data)

def createNewFileForJSON(jsonFileName, fileCount, jsonDataArray):
    new_file_name = jsonFileName + "_count_" + str(fileCount)
    if os.access(new_file_name, os.R_OK):
        print ("Source File : " + new_file_name + " is removed")
        if os.access(new_file_name, os.W_OK):
            os.remove(new_file_name)
        else:
            print (new_file_name + " is not Writeable and cannot be removed")
            return
    with open(new_file_name, 'w') as new_file_name_des:
        print(new_file_name)
        writeRecordToFile(jsonDataArray, new_file_name_des)

def readRawTextFile(fileName, jsonFileName):
    with open(fileName, 'r') as file_name_des:
        count = 0
        file_count = 0
        json_data_array = []
        first_line = True
        for line in file_name_des:
            count += 1
            line = line.replace("\n","")
            if count == 1 and first_line:
                row = line.split("\t")
                first_line = False
                print ("First Row = " + str(row))
            else:
                row = line.split("\t")
                if validateRecord(row):
                    print ("Bad line = " + (line))
                else:
                    json_data_array.append(createJSONRecord(row))
                    if count == ROW_COUNT_PER_FILE:
                        if len(json_data_array) > 0:
                            file_count += 1
                            createNewFileForJSON(jsonFileName, file_count, json_data_array)
                            count = 0 
                            json_data_array = []

        if len(json_data_array) > 0:
            file_count += 1
            createNewFileForJSON(jsonFileName, file_count, json_data_array)
            

if __name__ == '__main__':
    try:
        prog_des = "translate text file to JSON file"
        parser = argparse.ArgumentParser("PROG", description=prog_des)
        parser.add_argument("-f", "--textf", help="input text file name", required=True)
        parser.add_argument("-j", "--jsonf", help="output json file name", required=True)
        args = parser.parse_args()
        input_file_name = ""
        if not args.textf is None:
            input_file_name = args.textf
        output_file_name = ""
        if not args.jsonf is None:
            output_file_name = args.jsonf

        if input_file_name == "" or output_file_name == "":
            print ("Error with arguments for input or output file")
            exit(1)

        readRawTextFile(input_file_name, output_file_name)
  
    except NameError as ex:
        print ("Name error : " + str(ex))
        exit(1)
    except RuntimeError as ex:
        print ("Runtime Error : " + str(ex))
        exit(1)
    except Exception as ex:
        print ("Exception caught : " + str(ex))
        exit(1)
    exit(0)
    
