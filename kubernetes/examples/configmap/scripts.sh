# 1. kubectl create configmap
kubectl create configmap sport --from-literal=sport=football

# 2. kubectl create another configmap
kubectl create configmap sport --from-literal=fruit=apple