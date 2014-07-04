"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from as_status.models import Server, Process, ProcessStatus
from as_status.serializers import ServerSerializer, ProcessSerializer, ProcessStatusSerializer
#from as_status.views import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    def test_as_status(self):
        #Server(server_id=1, host_name="server1", is_virtual=False).save()
        s1 = Server.objects.get(pk=1)
        serializer = ServerSerializer(s1)
        print serializer.data
        
        #Process(process_id=1, name="java-api", type="as-core").save()
        p1 = Process.objects.get(pk=1)
        serializer2 = ProcessSerializer(p1)
        print serializer2.data
        
        ps1 = ProcessStatus.objects.get(pk=1)
        serializer3 = ProcessStatusSerializer(ps1)
        print serializer3.data

        