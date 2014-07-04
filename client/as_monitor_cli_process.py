
import httplib2, base64, json, socket, sys, subprocess, time
from optparse import OptionParser

# For global variables
USER = PASSWD = SERVER_HOST = ""
#HOST_NAME=socket.gethostname()
HOST_NAME = 'YES_TEST_HOST2'

usage = "usage: as_monitor_cli_process.py [update] $SERVER_ADDR $USER_NAME $PASSWORD | \n"
usage = usage + "                                 [list-process] $SERVER_ADDR, $USER_NAME, $PASSWORD | \n"
usage = usage + "                                 [register-process] $SERVER_ADDR, $USER_NAME, $PASSWORD $NAME $TYPE | \n"
usage = usage + "                                 [delete-process] $SERVER_ADDR, $USER_NAME, $PASSWORD $PROCESS_ID "
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()



def checkAuth(contents):
    if (str(contents).find("Invalid username") != -1):
        print "Invalid username / password. Check your authentication information"
        sys.exit()

def requestHttp(method, url, content):
    h = httplib2.Http()
    h.add_credentials(USER, PASSWD)
    auth = base64.encodestring(USER + ':' + PASSWD)
    resp, contents = h.request(url, method, headers = { 'Authorization' : 'Basic ' + auth , 'Content-type' : 'application/json' }, body = content)    
    
    if resp["status"] != "200" and resp["status"] != "400" and resp["status"] != "201" and resp["status"] != "204":
        #print "RESP: " + str(resp)
        #print "CONTENTS: " + str(contents)
        print "Respond STATUS: " + resp["status"] + "\nRespond status is not 200, 201 or 400 or in getHTTP call to : " + url
    checkAuth(contents)
    return contents

def getMyServerId():
    serverList = requestHttp("GET", SERVER_HOST + "/server/", None)
    jdata = json.loads(serverList)
    # For test only
    for i in jdata:
        if i['host_name'] == HOST_NAME:
            return i['id']

def checkArguments():
    if len(args) == 0 or (args[0] != "update" and args[0] != "list-process" and args[0] != "register-process" and args[0] != "delete-process"):
        #print "ERROR: specify [ update | list-process | register-process | delete-process ] in the first argument."
        parser.print_help()
        return False
    elif args[0] == "update":
        if len(args) != 4:
            print "ERROR: update - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD \n"
            parser.print_help()
            return False
    elif args[0] == "list-process":
        if len(args) != 4:
            print "ERROR: list-process - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD \n"
            parser.print_help()
            return False
    elif args[0] == "register-process":
        if len(args) != 6:
            print "ERROR: register-process - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD, $NAME, $TYPE \n"
            parser.print_help()
            return False
    elif args[0] == "delete-process":
        if len(args) != 5:
            print "ERROR: delete-process - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD, $PROCESS_ID \n"
            parser.print_help()
            return False

    global SERVER_HOST, USER, PASSWD
    SERVER_HOST = args[1]
    USER = args[2]
    PASSWD = args[3]

    if SERVER_HOST[-1:] == "/":
        SERVER_HOST = SERVER_HOST[:-1]

    return True

def update():
    myServerId = getMyServerId()
    #print " - myServerId: " + str(myServerId)
    if (myServerId == None):
        print "The server (" + HOST_NAME + ") is not registered.. Register the server first. "
        sys.exit()
    else:
        processList = requestHttp("GET", SERVER_HOST + "/process/", None)
        processesInAs = json.loads(processList)
        allprocess = myAllProcesses()
        for process in processesInAs:
            numOfProcess = checkMyProcess(allprocess, process["name"])
            if numOfProcess > 0:
                updateProcess(myServerId, process["id"], numOfProcess, time.strftime("%c"))

def updateProcess(serverId, processId, status, cdate):
#    print "UpdateProcess: " + str(serverId) + ", " + str(processId) + ", " + str(status) + ", " + cdate
    update_info = {"server": str(serverId), "process": str(processId), "status": str(status), "last_updated": str(cdate) }
    updateProcess = ""
    alreadyUpdate = False
    processStatusList = requestHttp("GET", SERVER_HOST + "/processStatus/", None)
    processStatusInAs = json.loads(processStatusList)
    for processStatus in processStatusInAs:
        if str(processStatus["server"]) == str(serverId) and str(processStatus["process"]) == str(processId):
            processStatusId = str(processStatus["id"])
            updateProcess = requestHttp("PUT", SERVER_HOST + "/processStatus/" + processStatusId , json.dumps(update_info))
            alreadyUpdate = True
            break
    if alreadyUpdate == False:
        updateProcess = requestHttp("POST", SERVER_HOST + "/processStatus/" , json.dumps(update_info))
    
    print "RETURN from the server: " + updateProcess

def myAllProcesses():
    command = ["ps", "-ef" ]
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print "Error in executing ps -ef .. May be not installed ps package. Exiting the program now.."
        sys.exit()
    sout = str(proc.stdout.read())
    return sout

def checkMyProcess(allprocess, processName):
    found = 0
    processSplit = allprocess.splitlines()
    for line in processSplit:
        if str(line).find(processName) != -1:
            found = found + 1
    return found

def register():
    reg_info = {"name": args[4], "type": args[5] }
    registerProcess = requestHttp("POST", SERVER_HOST + "/process/" , json.dumps(reg_info))
    print "RETURN from the server: " + registerProcess

def delete():
    process_id = args[4]
    deleteProcess = requestHttp("DELETE", SERVER_HOST + "/process/" + str(process_id) , "")
    print "RETURN from the server: " + deleteProcess

def listProcess():
    processList = requestHttp("GET", SERVER_HOST + "/process/", None)
    jdata = json.loads(processList)
    # For test only
    for i in jdata:
        print "- id: " + str(i["id"]) + ", name: " + i["name"] + " ,type: " + i["type"] + "" 


# -- Main -- #
if __name__ == '__main__':
    if checkArguments() == False:
        sys.exit()
    if (args[0] == "update"):
        update()
    elif (args[0] == "list-process"):
        listProcess()
    elif (args[0] == "register-process"):
        register()
    elif (args[0] == "delete-process"):
        delete()
        
        
    

    
