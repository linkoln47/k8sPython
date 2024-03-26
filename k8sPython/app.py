from configuration import *
from flask import Flask, render_template, json
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='template')
cors=CORS(app)
app.config['CORS_HEADER']='Content-Type'
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
    ns = v1.list_namespace()

    namespace = [i.metadata.name for i in ns.items]

    #response = app.response_class(response=json.dumps(namespace), status=200, mimetype='application/json')

    return namespace

@app.get("/pods/<id>")
def pods(id):
    pods = v1.list_namespaced_pod(namespace=id)

    return [i.metadata.name for i in pods.items]


@app.get("/deployment/<id>")
def deployment(id: str):
    dep = v1A.list_namespaced_deployment(namespace=id)

    return [i.metadata.name for i in dep.items]

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
    
@app.errorhandler(404)
def not_found(error):
    return render_template('page_not_found.html'), 404