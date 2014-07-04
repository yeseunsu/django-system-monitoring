
import httplib2, base64, json, socket, sys, subprocess, time
from optparse import OptionParser
from math import ceil

# For global variables
USER = PASSWD = SERVER_HOST = ""
#HOST_NAME=socket.gethostname()
HOST_NAME = 'YES_TEST_HOST2'

usage = "usage: as_monitor_cli_server.py [update] $SERVER_ADDR $USER_NAME $PASSWORD [options] | \n"
usage = usage + "                                [list-server] $SERVER_ADDR, $USER_NAME, $PASSWORD \n"
usage = usage + "                                [delete-server] $SERVER_ADDR, $USER_NAME, $PASSWORD $SERVER_ID\n"
usage = usage + "                                [register-server] $SERVER_ADDR, $USER_NAME, $PASSWORD $PUBLIC_IP $PRIVATE_IP $IS_VIRTUAL (true|false) $TYPE (as-core|as-lb) "
parser = OptionParser(usage=usage)
parser.add_option("-d", "--disk-for-data-mnt-dir", action="store", dest="data_mnt_dir", default="/data", type="string",  help="The second disk mount point to be monitored (default :/data)")
#parser.add_option("-p", "--process", action="store", dest="process", type="string", help="process type should be specified")
(options, args) = parser.parse_args()

SECOND_DISK_MNT_DIR = options.data_mnt_dir

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

def runCommand(command):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except:
        print "Error in executing sar.. May be not installed sysstat package. Exiting the program now.."
        sys.exit()
    return p


def getSystemInfo(info):
    # Get cpu, memory, sockets information
    command = ["sar", "-u", "-r", "-n", "SOCK", "1", "1"]
    p = runCommand(command)
    catch = "None"
    for line in iter(p.stdout.readline, b''):
        if (str(line).find("Average") != -1):
            word = line.split()
            if (catch == "CPU"):
                info["cpu"] = str(ceil ( float(word[2]) + float(word[4]) ) * 100 / 100.0)
                catch = "None"
            elif (catch == "Memory"):
                info["memory"] = word[3]
                catch = "None"
            elif (catch == "Socket"):
                info["sockets"] = word[1]
                catch = "None"
            else:
                word = line.split()
                if word[1] == "CPU":
                    catch = "CPU"
                elif (word[1] == "kbmemfree"):
                    catch = "Memory"
                elif (word[1] == "totsck"):
                    catch = "Socket"
                else:
                    pass
                continue

def getDiskStatus(info):
    # Get disk information
    command = ["df", "-h", "/"]
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except:
        print "Error in executing df.. May be not installed df package. Exiting the program now.."
        sys.exit()
    for line in iter(p.stdout.readline, b''):
        word = str(line).split()
        if word[len(word) - 1] == "/":
            info["disk_0"] = word[4][:-1]
            break

def getDiskStatus_second(info):
    # Get disk information
    command = ["df", "-h", SECOND_DISK_MNT_DIR]
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except:
        print "Error in executing df.. Exiting the program now.."
        sys.exit()
    
    for line in iter(p.stdout.readline, b''):
        if str(line).find("No such file or directory") != -1:
            info["disk_1"] = "n/a"
            return            
        word = str(line).split()
        if word[len(word) - 1] == SECOND_DISK_MNT_DIR:
            info["disk_1"] = word[4][:-1]
            break

def getServerStatus():
    info = {}
    ctime = time.strftime("%c")
    info["last_updated"] = str(ctime)
    getSystemInfo(info)
    getDiskStatus(info)
    getDiskStatus_second(info)

    return info

def updateServerStatus(serverStatusData, serverId):
    updateServerStatus = ""
    alreadyUpdate = False
    serverStatusList = requestHttp("GET", SERVER_HOST + "/serverStatus/", None)
    serverStatusInAs = json.loads(serverStatusList)
    for serverStatus in serverStatusInAs:
        if str(serverStatus["server"]) == str(serverId):
            serverStatusId = str(serverStatus["id"])
            updateServerStatus = requestHttp("PUT", SERVER_HOST + "/serverStatus/" + serverStatusId , serverStatusData)
            alreadyUpdate = True
            break
    if alreadyUpdate == False:
        updateServerStatus = requestHttp("POST", SERVER_HOST + "/serverStatus/" , serverStatusData)
    
    print "RETURN from the server: " + str(updateServerStatus)


def checkArguments():
    if len(args) == 0 or (args[0] != "update" and args[0] != "register-server" and args[0] != "list-server" and args[0] != "delete-server"):
       # print "ERROR: specify [ update | register-server | list-server | delete-server ] in the first argument."
        parser.print_help()
        return False
    elif args[0] == "update":
        if len(args) != 4:
            print "ERROR: update - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD \n"
            parser.print_help()
            return False
    elif args[0] == "list-server":
        if len(args) != 4:
            print "ERROR: register-server - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD \n"
            parser.print_help()
            return False
    elif args[0] == "delete-server":
        if len(args) != 5:
            print "ERROR: delete-server - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD $SERVER_ID \n"
            parser.print_help()
            return False
    elif args[0] == "register-server":
        if len(args) != 8:
            print "ERROR: register-server - specify correct $SERVER_ADDR, $USER_NAME, $PASSWORD, $PUBLIC_IP, $PRIVATE_IP, $IS_VIRTUAL (true | false), $TYPE (as-core|as-lb) \n"
            parser.print_help()
            return False
        else:
            if args[6] != "true" and args[6] != "false":
                print "ERROR: register-server - $IS_VIRTUAL should be 'true' or 'false'"
                parser.print_help()
                return False
            if args[7] != "as-core" and args[7] != "as-lb":
                print "ERROR: register-server - $TYPE should be 'as-core' or 'as-lb'"
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
        serverStatus = getServerStatus()
        serverStatus["server"] = myServerId
        updateServerStatus(json.dumps(serverStatus), myServerId)

def register_server():
    reg_info = dict()
    if args[6] == "true":
        reg_info = {"host_name": HOST_NAME ,"ip_addr_pub": args[4], "ip_addr_pri": args[5], "is_virtual": "True", "type": args[7] }
    else:
        reg_info = {"host_name": HOST_NAME, "ip_addr_pub": args[4], "ip_addr_pri": args[5], "is_virtual": "False", "type": args[7] }
        
    registerServer = requestHttp("POST", SERVER_HOST + "/server/" , json.dumps(reg_info))
    print "RETURN from the server: " + registerServer
    

def list_server():
    serverList = requestHttp("GET", SERVER_HOST + "/server/", None)
    jdata = json.loads(serverList)
    # For test only
    for i in jdata:
        sList = "Id: " + str(i["id"]) + ",   Hostname: " + i["host_name"] + ",   Ip_addr_pub: " + i["ip_addr_pub"] + ",   Ip_addr_pri: " 
        sList = sList + i["ip_addr_pri"] + ",   Is_virtual: " + str(i["is_virtual"]) + ",   Type:" + i["type"]
        print sList

def delete_server():
       
    server_id = args[4]
    deleteServer = requestHttp("DELETE", SERVER_HOST + "/server/" + str(server_id) , "")
    print "RETURN from the server: " + deleteServer

# -- Main -- #
if __name__ == '__main__':
    if checkArguments() == False:
        sys.exit()
    if args[0] == "update":
        update()
    elif args[0] == "register-server":
        register_server()
    elif args[0] == "list-server":
        list_server()
    elif args[0] == "delete-server":
        delete_server()
        
        
    

    
