from as_status.models import Server, Process, ProcessStatus, ServerStatus, OpenstackServiceStatus, OpenstackResourceStatus, ZnodeStatus, MongoStatus
from as_status.serializers import ServerSerializer, ProcessSerializer, ProcessStatusSerializer, ServerStatusSerializer, OpenstackServiceStatusSerializer, OpenstackResourceStatusSerializer, ZnodeStatusSerializer, MongoStatusSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def server_list(request):
    if request.method == 'GET':
        server = Server.objects.all()
        serializer = ServerSerializer(server, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ServerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def server_detail(request, pk):
    try:
        server = Server.objects.get(pk=pk)
    except Server.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServerSerializer(server)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ServerSerializer(server, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET', 'POST'])
def process_list(request):
    if request.method == 'GET':
        process = Process.objects.all()
        serializer = ProcessSerializer(process, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProcessSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def process_detail(request, pk):
    try:
        process = Process.objects.get(pk=pk)
    except Process.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProcessSerializer(process)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProcessSerializer(process, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        process.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def processStatus_list(request):
    if request.method == 'GET':
        processStatus = ProcessStatus.objects.all()
        serializer = ProcessStatusSerializer(processStatus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProcessStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def processStatus_detail(request, pk):
    try:
        processStatus = ProcessStatus.objects.get(pk=pk)
    except processStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProcessStatusSerializer(processStatus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProcessStatusSerializer(processStatus, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        processStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST'])
def serverStatus_list(request):
    if request.method == 'GET':
        serverStatus = ServerStatus.objects.all()
        serializer = ServerStatusSerializer(serverStatus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ServerStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def serverStatus_detail(request, pk):
    try:
        serverStatus = ServerStatus.objects.get(pk=pk)
    except serverStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServerStatusSerializer(serverStatus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ServerStatusSerializer(serverStatus, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        serverStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def openstackServiceStatus_list(request):
    if request.method == 'GET':
        openstackServiceStatus = OpenstackServiceStatus.objects.all()
        serializer = OpenstackServiceStatusSerializer(openstackServiceStatus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OpenstackServiceStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def openstackServiceStatus_detail(request, pk):
    try:
        openstackServiceStatus = OpenstackServiceStatus.objects.get(pk=pk)
    except openstackServiceStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OpenstackServiceStatusSerializer(openstackServiceStatus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OpenstackServiceStatusSerializer(openstackServiceStatus, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        openstackServiceStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def openstackResourceStatus_list(request):
    if request.method == 'GET':
        openstackResourceStatus = OpenstackResourceStatus.objects.all()
        serializer = OpenstackResourceStatusSerializer(openstackResourceStatus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OpenstackResourceStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def openstackResourceStatus_detail(request, pk):
    try:
        openstackResourceStatus = OpenstackResourceStatus.objects.get(pk=pk)
    except openstackResourceStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OpenstackResourceStatusSerializer(openstackResourceStatus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OpenstackResourceStatusSerializer(openstackResourceStatus, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        openstackResourceStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def znodeStatus_list(request):
    if request.method == 'GET':
        znodeStatus = ZnodeStatus.objects.all()
        serializer = ZnodeStatusSerializer(znodeStatus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ZnodeStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def znodeStatus_detail(request, pk):
    try:
        znodeStatus = ZnodeStatus.objects.get(pk=pk)
    except znodeStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ZnodeStatusSerializer(znodeStatus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ZnodeStatusSerializer(znodeStatus, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        znodeStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def mongoStatus_list(request):
    if request.method == 'GET':
        mongoStatus = MongoStatus.objects.all()
        serializer = MongoStatusSerializer(mongoStatus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MongoStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def mongoStatus_detail(request, pk):
    try:
        mongoStatus = MongoStatus.objects.get(pk=pk)
    except mongoStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MongoStatusSerializer(mongoStatus)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MongoStatusSerializer(mongoStatus, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mongoStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
