from kubernetes import client, config
from os import system, name
from configuration import *

v1 = client.CoreV1Api(client.ApiClient(configuration))
v1A= client.AppsV1Api(client.ApiClient(configuration))

print("Listing pods with their IPs:")
while(True):

    term = input("Welcome! Choose number(0-7): ")
    node = v1.list_node()
    pod = v1.list_pod_for_all_namespaces(watch=False)
    ns = v1.list_namespace()
    svc = v1.list_service_for_all_namespaces(watch=False)
    ret = v1.list_pod_for_all_namespaces(watch=False)
    match term:
        case '0':
            for i in node.items:
                name = i.metadata.name
                print("%s\t%s" % (i.metadata.name, i.status.conditions) )
        case '1':
            for i in ns.items:
                print("%s" % (i.metadata.name))
        case '2':
            pef = input("Choose namespace: ")
            pod = v1.list_namespaced_pod(namespace=pef)
            for i in pod.items:
                print("%s" % (i.metadata.name))
        case '3':
            for i in svc.items:
                print("%s" % (i.metadata.name))
        case '4':
            #id = input("Choose dep namespace: ")
            dep = v1A.list_deployment_for_all_namespaces()
            for i in dep.items:
                print("%s\t%s" % (i.metadata.namespace, i.metadata.name))
        case '5':
            for i in ret.items:
                print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        case '6':

            dep = v1A.list_deployment_for_all_namespaces()
            for i in dep.items:
                v1A.patch_namespaced_deployment_scale(
                    name=i.metadata.name, 
                    namespace='default', 
                    body = {'spec': {'replicas': 0}})
        case '7':

            dep = v1A.list_deployment_for_all_namespaces()
            for i in dep.items:
                v1A.patch_namespaced_deployment_scale(
                    name=i.metadata.name, 
                    namespace='default', 
                    body = {'spec': {'replicas': 1}})
        case 'exit':
            system('clear')
            break