from as_status.models import Server, Process, ProcessStatus, ServerStatus, OpenstackServiceStatus, OpenstackResourceStatus, ZnodeStatus, MongoStatus
from rest_framework import serializers

class ServerSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = Server
        fileds = ('host_name', 'ip_addr_pub', 'ip_addr_pri', 'is_virtual', 'type')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.host_name = attrs.get('host_name', instance.host_name)
            instance.ip_addr_pub = attrs.get('ip_addr_pub', instance.ip_pub)
            instance.ip_addr_pri = attrs.get('ip_addr_pri', instance.ip_pri)
            instance.is_virtual = attrs.get('is_virtual', instance.is_virtual)
            instance.type = attrs.get('type', instance.type)
            return instance
        return Server(**attrs)

class ProcessSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = Process
        fileds = ('name', 'type')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.name = attrs.get('name', instance.name)
            instance.type = attrs.get('type', instance.type)
            return instance
        return Process(**attrs)


class ProcessStatusSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = ProcessStatus
        fileds = ('server', 'process', 'status')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.server = attrs.get('server', instance.server)
            instance.process = attrs.get('process', instance.process)
            instance.status = attrs.get('status', instance.status)
            instance.last_updated = attrs.get('last_updated', instance.last_updated)
            return instance
        return ProcessStatus(**attrs)


class ServerStatusSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = ServerStatus
        fileds = ('server', 'cpu', 'memory', 'disk_0', 'disk_1', 'last_updated')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.server = attrs.get('server', instance.server)
            instance.cpu = attrs.get('cpu', instance.cpu)
            instance.memory = attrs.get('memory', instance.memory)
            instance.disk_0 = attrs.get('disk_0', instance.disk_0)
            instance.disk_1 = attrs.get('disk_1', instance.disk_1)
            instance.last_updated = attrs.get('last_updated', instance.last_updated)
            return instance
        return ServerStatus(**attrs)

class OpenstackServiceStatusSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = OpenstackServiceStatus
        fileds = ('service', 'host', 'status', 'state', 'last_updated')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.service = attrs.get('service', instance.service)
            instance.host = attrs.get('host', instance.host)
            instance.status = attrs.get('status', instance.status)
            instance.state = attrs.get('state', instance.state)
            instance.last_updated = attrs.get('last_updated', instance.last_updated)
            return instance
        return OpenstackServiceStatus(**attrs)

class OpenstackResourceStatusSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = OpenstackResourceStatus
        fileds = ('cores', 'memory', 'instances', 'ip', 'last_updated')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.cores = attrs.get('cores', instance.cores)
            instance.memory = attrs.get('memory', instance.memory)
            instance.instances = attrs.get('instances', instance.instances)
            instance.ip = attrs.get('ip', instance.ip)
            instance.last_updated = attrs.get('last_updated', instance.last_updated)
            return instance
        return OpenstackResourceStatus(**attrs)


class ZnodeStatusSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = ZnodeStatus
        fileds = ('name', 'path', 'count', 'contents', 'last_updated')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.name = attrs.get('name', instance.name)
            instance.path = attrs.get('path', instance.path)
            instance.count = attrs.get('count', instance.count)
            instance.contents = attrs.get('contents', instance.contents)
            instance.last_updated = attrs.get('last_updated', instance.last_updated)
            return instance
        return ZnodeStatus(**attrs)

class MongoStatusSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = MongoStatus
        fileds = ('host', 'health', 'status', 'last_updated')
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.host = attrs.get('host', instance.host)
            instance.health = attrs.get('health', instance.health)
            instance.status = attrs.get('status', instance.status)
            instance.last_updated = attrs.get('last_updated', instance.last_updated)
            return instance
        return MongoStatus(**attrs)
