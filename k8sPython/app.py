
from configuration import *
from flask import Flask

app = Flask(__name__)
v1 = client.CoreV1Api(client.ApiClient(configuration))
v1A= client.AppsV1Api(client.ApiClient(configuration))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/node")
def about():    
    namenode = ''
    node = v1.list_node()
    
    for i in node.items:
        data = {i.metadata.name: i.status.allocatable}

    return data

@app.get("/namespace")
def namespace():
    namespace = ''
    ns = v1.list_namespace()

    for i in ns.items:
        namespace += i.metadata.name + '\n'

    return namespace

@app.get("/pods/<id>")
def pods(id):
    namepods = ''
    pods = v1.list_namespaced_pod(namespace=id)

    for i in pods.items:
        namepods += i.metadata.name + '\n'

    return namepods


@app.get("/deployment/<id>")
def deployment(id: str):
    namedeployment = ''
    dep = v1A.list_namespaced_deployment(namespace=id)

    for i in dep.items:
        namedeployment += i.metadata.name + '\n'

    return namedeployment

@app.get("/<ns>/all/<id>")
def Odeployment(ns:str, id: bool):
    dep = v1A.list_namespaced_deployment(namespace=ns)

    if id:
        for i in dep.items:
            v1A.patch_namespaced_deployment_scale(
                name=i.metadata.name,
                namespace=ns,
                body = {'spec': {'replicas': 1}})
        return {"message": "Deployments on"}
    else:
        for i in dep.items:
            v1A.patch_namespaced_deployment_scale(
                name=i.metadata.name,
                namespace=ns,
                body = {'spec': {'replicas': 0}})
        return {"message": "Deployments off"}