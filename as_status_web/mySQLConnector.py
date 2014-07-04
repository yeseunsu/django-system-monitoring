'''
Created on Dec 9, 2013

@author: Eunsu Yun
'''

import MySQLdb
import sys, json
from operator import itemgetter

def getMysqlConnect():
    
    try:
        con = MySQLdb.connect('host', 'user', 'password', 'db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM tb1")
        devs = cur.fetchall()
        
        cur.execute("SELECT * FROM tb2")
        lbs = cur.fetchall()
        
        devices = []
        loadbalancers = []

        for device in devs:
            device_cont = dict()
            device_cont["id"] = device[0]
            device_cont["name"] = device[1]
            device_cont["type"] = device[2]
            device_cont["version"] = device[3]
            device_cont["ip"] = device[4]
            device_cont["port"] = device[5]
            device_cont["user"] = device[6]
            device_cont["password"] = device[7]
            device_cont["extra"] = device[8]
            devices.append(device_cont)
        
        for lb in lbs:
            lb_cont = dict()
            lb_cont["id"] = lb[0]
            lb_cont["device_id"] = lb[1]
            lb_cont["name"] = lb[2]
            lb_cont["algorithm"] = lb[3]
            lb_cont["protocol"] = lb[4]
            lb_cont["status"] = lb[5]
            lb_cont["tenant_id"] = lb[6]
            lb_cont["created_at"] = str(lb[7])
            lb_cont["updated_at"] = str(lb[8])
            lb_cont["deployed"] = lb[9]
            lb_cont["extra"] = lb[10]
            loadbalancers.append(lb_cont)
    
        aslb = []
        for device in devices:
            comb2 = []
            for loadbalancer in loadbalancers:
                if device.get("id") == loadbalancer.get("device_id"):
                    comb = dict()
                    comb["name"] = loadbalancer.get("name")
                    comb["id"] = loadbalancer.get("id")
                    comb["tenant_id"] = loadbalancer.get("tenant_id")
                    comb["created_at"] = loadbalancer.get("created_at")
                    comb["updated_at"] = loadbalancer.get("updated_at")
                    comb["extra"] = loadbalancer.get("extra")
                    comb["device_ip"] = device.get("ip")
                    comb["device_extra"] = device.get("extra")
                    comb2.append(comb)
            aslb_dict = dict()
            aslb_dict["name"] = device.get("name")
            aslb_dict["ip"] = device.get("ip")
            extra = json.loads(device.get("extra"))
            if "vip" in extra and extra["vip"] != "":
                aslb_dict["vip"] = extra["vip"]
            else:
                aslb_dict["vip"] = "None"
            aslb_dict["createdTime"] = extra["createdTime"]
            aslb_dict["lb"] = comb2
            aslb.append(aslb_dict)

   
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
        
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
    
    return sorted(aslb, key=itemgetter("createdTime"))
