# encoding: utf-8
# Greeting Bot
# Authors: <Rakesh Sachdeva <Rakesh.Sachdeva@careerbuilder.com>> <Singh, Prashant <Prashant.Singh@careerbuilder.com>>
'''
This library implement algorithm for greetings messages.

'''
####### Internal Library Import
import configparser
from extract_w2data import ExtractW2data
import validateDetails as valobj
import shutil, re

###### Generic Library Import
import sys

sys.path.insert(0, "../../")
# reload(sys)
# sys.setdefaultencoding('utf8')
from flask import Flask, jsonify
import json, requests
from flask_cors import CORS, cross_origin
from flask import json
from flask.globals import request
import os


config_file_loc = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config", "config.cfg")
if os.path.isfile(config_file_loc) == False:
    raise Exception("Failed to read the Config file from the location: " + str(config_file_loc))

config_obj = configparser.ConfigParser()
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

try:

    config_obj.read(config_file_loc)
    server_add = (config_obj.get("serverdetails", "server_add"))
    port_num = (config_obj.get("serverdetails", "port_num"))
    inputPdfFolderPath = (config_obj.get("filepaths", "inputPdfFolderPath"))
    inputImgsFolderPath = (config_obj.get("filepaths", "inputImgsFolderPath"))
    ConvertedImgsPath = (config_obj.get("filepaths", "ConvertedImgsPath"))

    logfilename = config_obj.get("logdata", "logfilename")
    # apiPort=config_obj.get("REST","port")
except Exception as e:
    raise Exception("Config file reading error: " + str(e))

app = Flask(__name__)
CORS(app)
w2_obj = ExtractW2data()


def Merge(status, response):
    return (status.update(response))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






#
# # ------------------------------------------------------------------------------------------------------------------------------------
@app.route('/extract-w2-data', methods=['POST'])
@cross_origin()
def processw2Api():
    inputRequestFomat = {
        "data": [{"filePath": "w2_file_path", "documentId": 1001,"pageNum":1}, {"filePath": "w2_file_path2", "documentId": 1002,"pageNum":1}]}
    if request.method != 'POST':
        apireponse = {"status": 101, "error": "Only accept POST request"}
        Merge(apireponse, {})
        return json.dumps({"data": [apireponse]})

    if not request.headers['Content-Type'] == 'application/json':
        apireponse = {"status": 102, "error": "Only accept Content-Type:application/json in headers"}
        Merge(apireponse, {})
        return json.dumps({"data": [apireponse]})

    if not request.is_json:
        apireponse = {"status": 103,
                      "error": "Content_Type should be applicatin/json,Expecting json data key as : " + str(
                          inputRequestFomat)}
        Merge(apireponse, {})
        return json.dumps({"data": [apireponse]})
    if 'data' not in request.json:
        apireponse = {"status": 104, "error": "Expecting json, 'data' as  key eg : " + str(inputRequestFomat)}
        Merge(apireponse, {})
        return json.dumps({"data": [apireponse]})
    filenames = []
    documentIds = []
    page_num=[]
    for eachrequest in request.json['data']:
        if type(eachrequest) != dict or ('filePath' not in eachrequest) or ('documentId' not in eachrequest) or ('pageNum' not in eachrequest) :
            apireponse = {"status": 105, "error": "Expecting json, 'data' as key eg : " + str(inputRequestFomat)}
            Merge(apireponse, {})
            return json.dumps({"data": [apireponse]})
        elif type(eachrequest) == dict and 'filePath' in eachrequest and 'documentId' in eachrequest and 'pageNum' in eachrequest :
            filenames.append(eachrequest['filePath'])
            documentIds.append(eachrequest['documentId'])
            page_num.append(eachrequest['pageNum'])

    if len(filenames) != len(documentIds) or len(filenames)!=len(page_num):
        apireponse = {"status": 106,
                      "error": "Expecting json,with equal number 'documentid', 'filePath' and 'pageNum' in data key  : " + str(
                          inputRequestFomat)}
        Merge(apireponse, {})
        return json.dumps({"data": [apireponse]})

    apireponseList = []
    for indx, inpfilename in enumerate(filenames):
        try:

            if os.path.isfile(inpfilename) == False:
                apireponse = {"status": 107,
                              "error": ' file not exist as given path '}
                Merge(apireponse, {})
                apireponseList.append(apireponse)
            pfilename, pfile_extension = os.path.splitext(inpfilename)
            uniqid = os.path.basename(pfilename).split("-")[0]
            if pfile_extension.lower() == ".pdf":
                if int(page_num[indx]) not in range(1, 1000):
                    page_num[indx]=1
                responseData = w2_obj.process_w2(inpfilename,int(page_num[indx]))
                validated_response = valobj.validate_response(responseData, inpfilename, uniqid, documentIds[indx])
                apireponse = {"status": 200, "error": ""}
                Merge(apireponse, validated_response)
                apireponseList.append(apireponse)

                # return json.dumps({"data": [apireponse]})


            elif pfile_extension.lower() in [".jpg", ".jpeg", ".png"]:
                responseData = w2_obj.extract_img_data(inpfilename)
                validated_response = valobj.validate_response(responseData, inpfilename, uniqid, documentIds[indx])
                apireponse = {"status": 200, "error": ""}
                Merge(apireponse, validated_response)
                apireponseList.append(apireponse)

                # return json.dumps({"data": [apireponse]})

            else:
                apireponse = {"status": 109, "error": 'Expecting file formats : jpeg, jpg, png or pdf  '}
                Merge(apireponse, {})
                apireponseList.append(apireponse)

                # return json.dumps({"data":[apireponse]})

        except Exception as e:
            apireponse = {"status": 110, "error": 'W2  extraction error'}
            Merge(apireponse, {})
            apireponseList.append(apireponse)
    #print(apireponseList)
    return json.dumps({"data": apireponseList})


if __name__ == '__main__':
    app.run(server_add, port=(port_num), debug=False, threaded=True)
    # import requests, glob, os, json
    #
    # files = glob.glob("New_W2/*.*")
    # print(len(files))
    #
    # for index,x in enumerate(files):
    #     pfilename,pfile_extension=os.path.splitext(x)
    #     (pfilename)=str(os.getcwd()+"/"+x)
    #     if pfile_extension.lower() == ".pdf":
    #         responseData = w2_obj.process_w2(pfilename)
    #         validated_response = validate_response(responseData, pfilename, index, index)
    #         apireponse = {"status": 100, "error": ""}
    #     elif pfile_extension.lower() in [".jpg", ".jpeg", ".png"]:
    #         responseData = w2_obj.extract_img_data(pfilename)
    #         validated_response = validate_response(responseData, pfilename,  index, index)
