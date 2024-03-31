from configuration import *
from flask import Flask, render_template, session
from flask_cors import CORS

app = Flask(__name__, template_folder='template')
cors=CORS(app)
app.config['CORS_HEADER']='Content-Type'


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/node")
def about():    
    node = v1.list_node()
    
    for i in node.items:
        data = {i.metadata.name: i.status.allocatable}

    return data

@app.get("/namespace")
def namespace():
    ns = v1.list_namespace()

    namespace = [i.metadata.name for i in ns.items]

    return render_template("namespaces_list.html", namespace=namespace)

@app.get("/pods/<id>")
def pods(id: str):
    if (id == 'all'):
        all_pods = v1.list_pod_for_all_namespaces(watch=False)

        data = {
            "name": [i.metadata.name for i in all_pods.items],
            "namespace": [i.metadata.namespace for i in all_pods.items],
            "pod_ip": [i.status.pod_ip for i in all_pods.items]
        }

        return render_template("pods_list.html", pods=data)
    
    else:
        pods = v1.list_namespaced_pod(namespace=id)

        data = {
            "name": [i.metadata.name for i in pods.items],
            "pod_ip": [i.status.pod_ip for i in pods.items]
        }

        return render_template("pods_list.html", pods=data)

@app.get("/deployments/<id>")
def deployments(id: str):
    if (id == 'all'):
        all_deployments = v1A.list_deployment_for_all_namespaces(watch=False)

        data = {
            "name": [i.metadata.name for i in all_deployments.items],
            "namespace": [i.metadata.namespace for i in all_deployments.items],
            "replicas": [i.spec.replicas for i in all_deployments.items]
        }

        return render_template("deployments_list.html", deployments=data)
    
    else:
        deployments = v1A.list_namespaced_deployment(namespace=id)

        data = {
            "name": [i.metadata.name for i in deployments.items],
            "replicas": [i.spec.replicas for i in deployments.items]
        }

        return render_template("deployments_list.html", deployments=data)
    
@app.get("/services/<id>")
def services(id: str):
    if (id == 'all'):
        all_services = v1.list_service_for_all_namespaces(watch=False)
        
        data = {
            "name": [i.metadata.name for i in all_services.items],
            "namespace": [i.metadata.namespace for i in all_services.items],
            #"cluster_ip": [i.spec.clusterIP for i in all_services.items]
        }
        
        return render_template("services_list.html", services=data)
    
    else:
        services = v1.list_namespaced_service(namespace=id)

        data = {
            "name": [i.metadata.name for i in services.items]
        }

        return render_template("services_list.html", services=data)
    
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