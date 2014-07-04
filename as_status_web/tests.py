"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


from django.test import TestCase
from as_status_web.mySQLConnector import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
  
        for as_dev in getMysqlConnect():
            print "Device_name: " + as_dev["name"]
            print "Device ip: "  + as_dev["ip"]
            print "Device_vip: " + str(as_dev["vip"])
            print "Device_create_time: " + str(as_dev["createdTime"])
            for lb in as_dev["lb"]:
                print " - LB name: " + lb["name"]
                print "      -- tenant_id: " + lb["tenant_id"]
                print "      -- extra: " + lb["extra"]
            print "\n"