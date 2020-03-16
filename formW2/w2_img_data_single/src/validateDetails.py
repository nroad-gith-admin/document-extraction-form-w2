import re

def empid_response(empidres):
    if len(empidres) == 0:
        return "", "Fail:Value not Extracted"

    if isinstance(empidres, list) and len(empidres) > 0:
        empidres = empidres[0]
    elif isinstance(empidres, list) and len(empidres) == 0:
        return "", "Fail:Value not Extracted"

    empidres = empidres.replace(" ", "")

    if re.findall("\s+[0-9]{2}\s*\-\s*[0-9]{7}\s+", " " + empidres + " ") or re.findall("\s+[0-9]{9}\s+",
                                                                                        " " + empidres + " "):
        return empidres, "Pass"
    else:
        return "", "Fail:Value not Extracted"

def w2_str_features(responseFeature, mincharlimit):
    if isinstance(responseFeature, str) == True and len(responseFeature) > mincharlimit:
        return responseFeature, "Pass"
    else:
        return "", "Fail:Value not Extracted"

def year_response(responseYear):
    if len(responseYear) == 0:
        return 0, "Fail:Value not Extracted"
    if isinstance(responseYear, list) and len(responseYear) > 0:
        responseYear = responseYear[0]
    elif isinstance(responseYear, list) and len(responseYear) == 0:
        return 0, "Fail:Value not Extracted"
    responseYear = (responseYear.replace(" ", ""))
    if len(responseYear) == 4 and isinstance(int(responseYear), int):
        return int(responseYear), "Pass"
    else:
        return 0, "Fail:Value not Extracted"


def wages_response(wages):
    if wages == 0:
        return 0.0, "Pass"
    elif wages == -9999.99:
        return -9999.99, "Fail:Value not Extracted"

    wages = wages.replace(" ", "")
    if re.findall(r"\s+[0-9]+\s*\.\s*[0-9]{2}\s+", " " + str(wages) + " ") or int(wages) == 0:
        return float("{0:.2f}".format(float(wages))), "Pass"

    else:
        return -9999.99, "Fail:Value not Extracted"

def validate_response(responsedata, inpfilename, uniqid, docid):
    validated_res = {}
    validated_res["documentId"] = docid
    #validated_res["filename"] = inpfilename
    #validated_res["uniqueId"], validated_res["uniqueIdStatus"] = w2_str_features(uniqid, mincharlimit=17)
    validated_res["employerName"], validated_res["employerNameStatus"] = w2_str_features(responsedata["employer name"],
                                                                                         mincharlimit=3)
    validated_res["employeeName"], validated_res["employeeNameStatus"] = w2_str_features(responsedata["employee name"],
                                                                                         mincharlimit=5)
    validated_res["employeeAddress"], validated_res["employeeAddressStatus"] = w2_str_features(responsedata["employeeAdd"],
                                                                                         mincharlimit=5)
    #validated_res["filename"], validated_res["filenameStatus"] = w2_str_features(inpfilename, mincharlimit=21)
    validated_res["year"], validated_res["yearStatus"] = year_response(responsedata["year"])
    validated_res["employerIdNumber"], validated_res["employerIdNumberStatus"] = empid_response(
        responsedata["employer id number"])
    validated_res["wagesTipsOtherComp"], validated_res["wagesTipsOtherCompStatus"] = wages_response(
        responsedata["wages tips other comp"])
    validated_res["socialSecurityWages"], validated_res["socialSecurityWagesStatus"] = wages_response(
        responsedata["social security wages"])
    validated_res["medicareWageAndTips"], validated_res["medicareWageAndTipsStatus"] = wages_response(
        responsedata["medicare wages and tips"])

    if validated_res["employeeNameStatus"] != "Pass" and validated_res["wagesTipsOtherCompStatus"] != "Pass":
        validated_res["docStatus"] = "Fail"
    elif validated_res["employeeNameStatus"] == "Pass" and validated_res["wagesTipsOtherCompStatus"] == "Pass" and \
            validated_res["yearStatus"] == "Pass":
        validated_res["docStatus"] = "Success"
    elif (validated_res["employeeNameStatus"] == "Pass" and validated_res["wagesTipsOtherCompStatus"] == "Pass") or (
            validated_res["employeeNameStatus"] and validated_res["yearStatus"] == "Pass") or (
            validated_res["wagesTipsOtherCompStatus"] == "Pass" and validated_res["yearStatus"] == "Pass"):
        validated_res["docStatus"] = "Partial Success"
    else:
        validated_res["docStatus"] = "Partial Success"

    return validated_res