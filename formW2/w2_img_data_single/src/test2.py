import re
ele='nee capra gross pay 46769.44 46769.44 46769.44 46769.44 uluhi 96825 plus third party sick pay 186000 1860.00 1860.00 1860.00'

junks=["state income tax","a. employee soc. sec. no.","7 social security tips 8 allocated tips"]

def removeEmployeeAddJunk( employeeAdd):
    for eachjunk in junks:
        if eachjunk in employeeAdd:
            employeeAdd = employeeAdd.replace(eachjunk, "")
    floatvalues = re.findall(r'[0-9]+[.]+[0-9]+', employeeAdd)
    for eachfloat in floatvalues:
        employeeAdd = employeeAdd.replace(eachfloat, "")

    return employeeAdd[:50].strip()


print(removeEmployeeAddJunk( ele))


