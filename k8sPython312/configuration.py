from kubernetes import client

secret_key = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ik9mYzFJSGtxWlk1UXFXblJ2MFk1elZvMDZZcXpvYkFIcTRiMzVmN0w5NVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMjI0MDYxMjItNjJmZS00YjlhLTgzYzctZWY3Y2VlZWU5YTA0Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRlZmF1bHQifQ.SZugis12soIXWB9YrquvXdUeiRUS2OMruoOHB607FQOY5Nxr9o-3MHVwVUUIHG6jpn5BSbJK3TfBTK1REDOE8FGhthD7Znc1euf-EvXKgBylvc2QhO4oqm_XOiKQBBuVwLYMmMK4JBT3dJf8MXQRczt9kiQdT3zEUXvDKmyUtYAqeru0FwtOGbOiWc8aP2G0MsEN8HtXtUwsft-RCcuIuthYcXI4E2KPm6m-N3w00F5bM91Uq9B5C65SmfQHHCUKKb55zMin0Mx7-UdZpER3Vx_AAKWA6EzoVDtkiSmLe446tLOJOKmS8uXeE6rtCYN4dqdBAdV4QiZUIH-draG65g'

configuration = client.Configuration() #Init client

configuration.api_key["authorization"] = secret_key
configuration.api_key_prefix['authorization'] = 'Bearer'    #header authorization prefix
configuration.host = 'https://192.168.59.100:8443'          #'https://192.168.59.100' host_api
configuration.ssl_ca_cert= '/home/linkoln/.minikube/ca.crt' #Cert_Check

v1 = client.CoreV1Api(client.ApiClient(configuration))
v1A= client.AppsV1Api(client.ApiClient(configuration))