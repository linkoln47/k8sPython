from configuration import *
from flask import Flask, render_template, session, redirect, request, url_for

app = Flask(__name__, template_folder='template')
app.config['CORS_HEADER']='Content-Type'
app.secret_key = secret_key


@app.get("/")
def read_root():
    return render_template("index.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form["nm"]
        password = request.form["pswd"]
        if user == "root" and password == "root":
            session["user"] = user
            session["password"] = password
            return redirect(url_for("user"))
        else:
            return redirect(url_for("login"))
    else:
        if "user" in session and "password" in session:
            return redirect(url_for("user"))
        return render_template("login.html")
    
@app.get("/logout")
def logout():
    session.pop("user", None)
    session.pop("password", None)
    return redirect(url_for("login"))
    
@app.get("/user")
def user():
    if "user" in session and "password" in session:
        user = session["user"]
        password = session["password"]
        return f"<h1>{user} {password}</h1>"
    else:
        return redirect(url_for("login"))

@app.get("/node")
def about():
    if "user" in session and "password" in session:
        node = v1.list_node()

        for i in node.items:
            data = {i.metadata.name: i.status.allocatable}
        return data
    else:
        return redirect(url_for("login"))

@app.get("/namespace")
def namespace():
    if "user" in session and "password" in session:
        ns = v1.list_namespace()

        namespace = [i.metadata.name for i in ns.items]

        return render_template("namespaces_list.html", namespace=namespace)
    else:
        return redirect(url_for("login"))

@app.get("/pods/<id>")
def pods(id: str):
    if "user" in session and "password" in session:
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
    else:
        return redirect(url_for("login"))

@app.get("/deployments/<id>")
def deployments(id: str):
    if "user" in session and "password" in session:
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
    else:
        return redirect(url_for("login"))
    
@app.get("/services/<id>")
def services(id: str):
    if "user" in session and "password" in session:
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
    else:
        return redirect(url_for("login"))
    
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