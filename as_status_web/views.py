from as_status.models import Server, Process, ProcessStatus, ServerStatus, OpenstackServiceStatus,OpenstackResourceStatus, ZnodeStatus, MongoStatus
from django.shortcuts import render
from as_status_web.mySQLConnector import *
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    
    # declare objects
    server_list = Server.objects.order_by('host_name').all()
    process_list = Process.objects.order_by('type').all()
    processStatus_list = ProcessStatus.objects.order_by('server__host_name').all()
    serverStatus_list = ServerStatus.objects.order_by('server__host_name').all()
    openstackServiceStatus_list = OpenstackServiceStatus.objects.order_by('service').all()
    openstackResourceStatus_list = OpenstackResourceStatus.objects.all()
    znodeStatus_list = ZnodeStatus.objects.all()
    mongoStatus_list = MongoStatus.objects.order_by('host').all()

    # For Load Balancer List    
    lb_list = getMysqlConnect()
    
    context = {'server_list': server_list, 
               'process_list': process_list,
               'processStatus_list': processStatus_list,
               'serverStatus_list': serverStatus_list,
               'openstackServiceStatus_list': openstackServiceStatus_list,
               'openstackResourceStatus_list': openstackResourceStatus_list,
               'znodeStatus_list': znodeStatus_list,
               'mongoStatus_list': mongoStatus_list,
               'lb_list': lb_list
               }
    
    return render(request, 'as_status_web/as_status_all.html', context)