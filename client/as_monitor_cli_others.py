
# For debugging and test only
TEST = 1

# For znode lookup data. Change this if needed
ZNODE_DATA = {"master": ["znode_path_1", "d1"],
              "proxy": ["znode_path_2", "d2"],
              "api": ["znode_path_3", "d3"]}


import httplib2, base64, json, sys, subprocess, time
from optparse import OptionParser

# For global variables
USER = PASSWD = SERVER_HOST = ""

usage = "usage: as_monitor_cli_others.py [update-znode] $SERVER_ADDR $USER_NAME $PASSWORD $PATH_TO_ZK_BIN| \n"
usage = usage + "                                 [update-openstack-service] $SERVER_ADDR, $USER_NAME, $PASSWORD | \n"
usage = usage + "                                 [update-openstack-resource] $SERVER_ADDR, $USER_NAME, $PASSWORD $PATH_TO_SCRIPT| \n"
usage = usage + "                                 [update-mongo] $SERVER_ADDR, $USER_NAME, $PASSWORD $MONGO_REST_PATH"
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()


def checkAuth(contents):
    if (str(contents).find("Invalid username") != -1):
        print "Invalid username / password. Check your authentication information"
        sys.exit()

def requestHttp(method, url, content):
    h = httplib2.Http(timeout=2)
    h.add_credentials(USER, PASSWD)
    auth = base64.encodestring(USER + ':' + PASSWD)
    resp, contents = h.request(url, method, headers = { 'Authorization' : 'Basic ' + auth , 'Content-type' : 'application/json' }, body = content)    
    
    if resp["status"] != "200" and resp["status"] != "400" and resp["status"] != "201" and resp["status"] != "204":
        #print "RESP: " + str(resp)
        #print "CONTENTS: " + str(contents)
        print "Respond STATUS: " + resp["status"] + "\nRespond status is not 200, 201, 204 or 400 or in getHTTP call to : " + url
    checkAuth(contents)
    return contents


def checkArguments():
    if len(args) == 0 or (args[0] != "update-znode" and args[0] != "update-openstack-service" and args[0] != "update-openstack-resource" and args[0] != "update-mongo"):
        #print "ERROR: specify [ update | list-process | register-process | delete-process ] in the first argument."
        parser.print_help()
        return False
    elif args[0] == "update-znode":
        if len(args) != 5:
            parser.print_help()
            return False
    elif args[0] == "update-openstack-service":
        if len(args) != 4:
            parser.print_help()
            return False
    elif args[0] == "update-openstack-resource":
        if len(args) != 5:
            parser.print_help()
            return False
    elif args[0] == "update-mongo":
        if len(args) != 5:
            parser.print_help()
            return False

    global SERVER_HOST, USER, PASSWD
    SERVER_HOST = args[1]
    USER = args[2]
    PASSWD = args[3]

    if SERVER_HOST[-1:] == "/":
        SERVER_HOST = SERVER_HOST[:-1]

    return True


def updateZnodeStatus(znode_id, data):
    updateZnodeStatus = requestHttp("PUT", SERVER_HOST + "/znodeStatus/" + str(znode_id) , data)
    print "RETURN from the server: " + updateZnodeStatus


def createZnodeStatus(data):
    createZnodeStatus = requestHttp("POST", SERVER_HOST + "/znodeStatus/" , data)
    print "RETURN from the server: " + createZnodeStatus


def update_znode():
    path = args[4]
    if path[-1:] == "/":
        path = path[:-1]
    
    for key in ZNODE_DATA:
        command = ["sh", path + "/zkCli.sh", "ls", ZNODE_DATA[key][0]]
        count, contents = get_znode_result(command, ZNODE_DATA[key][1])
        #print "Size: " + count
        #print "Contents: " + contents
    
        znodeList = requestHttp("GET", SERVER_HOST + "/znodeStatus/", None)
        znodeListjson = json.loads(znodeList)
        found = False
        znodeData = {"name": key, "path": ZNODE_DATA[key][0], "count": str(count), "contents": contents, "last_updated": time.strftime("%c")}
        
        for znodeItem in znodeListjson:
            if znodeItem["name"] == key and znodeItem["path"] == ZNODE_DATA[key][0]:
                print "updatingZnodeStatus..."
                updateZnodeStatus(znodeItem["id"], json.dumps(znodeData))
                found = True
                break
        if found == False:
            print "creatingZnodeStatus..."
            createZnodeStatus(json.dumps(znodeData))
    
def run_command(command):
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print "Error in executing command:  " + command[0] + " > Exiting the program now.."
        sys.exit()
    sout = str(proc.stdout.read())
    return sout

def get_znode_result(command, grep_type):
    res = ""
    command_result = run_command(command)
    if len(command_result) == 0:
        print "cannot get the znode data.. check $PATH_TO_ZK_BIN (e.g. /usr/local/zookeeper/bin) exiting the program.."
        sys.exit()
            
    processSplit = command_result.splitlines()
    for line in processSplit:
        if str(line).find(grep_type) != -1:
            res = line
            break
    
    res_arr = res.split(",")
    return str(len(res_arr)), res
    

def update_openstack_service():
    cmd = ["nova-manage", "service", "list"]
    cmd_result = ""

    cmd_result = run_command(cmd)

    if len(cmd_result) == 0:
        print "Error in executing nova-manage. exiting the program.."
        sys.exit()
    
    
    initialPost, jsonResult = isInitialPost("openstackServiceStatus")
    ossJson = jsonResult
        
    processSplit = cmd_result.splitlines()
    for line in processSplit:
        if line.find("Binary") != -1 and line.find("Zone") != -1:
            continue
        else:
            words = line.split()
            data = {"service": words[0], "host": words[1], "status": words[3], "state": words[4], "last_updated": time.strftime("%c") + " (" + words[5] + " " + words[6] + ")"}
            rdata = json.dumps(data)
            if initialPost == True:
                respond = requestHttp("POST", SERVER_HOST + "/openstackServiceStatus/", rdata)
                print respond
            else:
                found = False
                for item in ossJson:
                    if (data["service"] == item["service"] and data["host"] == item["host"]):
                        found = True
                        respond = requestHttp("PUT", SERVER_HOST + "/openstackServiceStatus/" + str(item["id"]), rdata)
                        print respond
                        break
                if found == False:
                    respond = requestHttp("POST", SERVER_HOST + "/openstackServiceStatus/", rdata)
                    print respond
    

def update_openstack_resource():
    cmd_path = args[4]
    command = ["python", cmd_path]
    cmd_result = ""
    cmd_result = run_command(command)

    if len(cmd_result) == 0:
        print "Error in executing openstackResourceStatus script.. Check $PATH_TO_SCRIPT.  exiting the program.."
        sys.exit()

    resource_data = dict()
    items = cmd_result.split(",")
    for item in items:
        index = item.find(":")
        categ = item[:index].strip()
        value = item[index + 1:].strip()
        resource_data[categ] = value
    
    resource_data["last_updated"] = time.strftime("%c")
    initialPost = isInitialPost("openstackResourceStatus")
    
    if initialPost == True:
        respond = requestHttp("POST", SERVER_HOST + "/openstackResourceStatus/", json.dumps(resource_data))
        print respond
    else:
        respond = requestHttp("PUT", SERVER_HOST + "/openstackResourceStatus/1", json.dumps(resource_data))
        print respond
        
def isInitialPost(url_type):
    initialPost = False
    resourceList = requestHttp("GET", SERVER_HOST + "/" + url_type + "/", None)
    listJson = json.loads(resourceList)
    if len(listJson) == 0:
        initialPost = True
    return initialPost, listJson

def update_mongo():
    url = args[4]
    h = httplib2.Http(timeout=2)
    resp, contents = h.request(url, "GET")
    if resp["status"] != "200":
        print "Respond STATUS: " + resp["status"] + " to " + url + " --> Exiting the program.." 
        sys.exit()
    
    cjson = json.loads(contents)
    members = cjson["members"]
   
    initialPost, listJson = isInitialPost("mongoStatus")
   
    data = dict()
    for member in members:
        data["host"] = member["name"]
        data["health"] = member["health"]
        data["status"] = str(member["state"]) + " - " + member["stateStr"] + " - uptime: " + str(member["uptime"])
        data["last_updated"] = time.strftime("%c")
    
        if initialPost == True:
            respond = requestHttp("POST", SERVER_HOST + "/mongoStatus/", json.dumps(data))
            print respond
        else:
            found = False
            for item in listJson:
                if data["host"] == item["host"]:
                    found = True
                    respond = requestHttp("PUT", SERVER_HOST + "/mongoStatus/" + str(item["id"]), json.dumps(data))
                    print respond
                    break
            if found == False:
                respond = requestHttp("POST", SERVER_HOST + "/openstackServiceStatus/", json.dumps(data))
                print respond


# -- Main -- #
if __name__ == '__main__':
    if checkArguments() == False:
        sys.exit()
    if (args[0] == "update-znode"):
        update_znode()
    elif (args[0] == "update-openstack-service"):
        update_openstack_service()
    elif (args[0] == "update-openstack-resource"):
        update_openstack_resource()
    elif (args[0] == "update-mongo"):
        update_mongo()
        
        
    

    
