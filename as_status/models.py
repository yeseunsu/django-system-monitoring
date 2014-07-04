from django.db import models

# Create your models here.
class Server(models.Model):
    host_name = models.CharField(max_length=100)
    ip_addr_pub = models.CharField(max_length=100)
    ip_addr_pri = models.CharField(max_length=100)
    is_virtual = models.BooleanField(default=True)
    type = models.CharField(max_length=50)
    def __unicode__(self):
        return str(self.server_id) + ": " + self.host_name

class Process(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.process_id) + ": " + self.name
    
class ProcessStatus(models.Model):
    server = models.ForeignKey(Server)
    process = models.ForeignKey(Process)
    status = models.IntegerField()
    last_updated = models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.server) + ": " + str(self.process) + ": " + str(self.status)
    
class ServerStatus(models.Model):
    server = models.ForeignKey(Server)
    cpu = models.CharField(max_length=100)
    memory = models.CharField(max_length=100)
    disk_0 = models.CharField(max_length=100)
    disk_1 = models.CharField(max_length=100)
    last_updated = models.CharField(max_length=100)
    def __unicode__(self):
        str(self.server) + ": " + str(self.cpu) + ": " + str(self.memory) + ": " + str(self.disk_0) + ": " + str(self.disk_1)
        
class OpenstackServiceStatus(models.Model):
    service = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    last_updated = models.CharField(max_length=100)
    def __unicode__(self):
        str(self.service) + ": " + str(self.server) + ": " + str(self.status) + ": " + str(self.state)
    
class OpenstackResourceStatus(models.Model):
    cores = models.CharField(max_length=100)
    memory = models.CharField(max_length=100)
    instances = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    last_updated = models.CharField(max_length=100)
    def __unicode__(self):
        str(self.cores) + ": " + str(self.memory) + ": " + str(self.instances) + ": " + str(self.ip)


class ZnodeStatus(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    count = models.IntegerField()
    contents = models.CharField(max_length=1000)
    last_updated = models.CharField(max_length=100)
    def __unicode__(self):
        str(self.name) + ": " + str(self.path) + ": " + str(self.count) + ": " + str(self.contents)

class MongoStatus(models.Model):
    host = models.CharField(max_length=100)
    health = models.IntegerField()
    status = models.CharField(max_length=100)
    last_updated = models.CharField(max_length=100)
    def __unicode__(self):
        str(self.host) + ": " + str(self.health) + ": " + str(self.status)
