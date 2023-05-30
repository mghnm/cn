# Dependencies

## Charts

The charts we are using are the following:

- postgresql-12.1.3 from [bitnami](https://charts.bitnami.com/bitnami). `helm repo add bitnami https://charts.bitnami.com/bitnami` 
- From same repo as above we get grafana-8.2.20


- prometheus-19.0.2 (community) from [prometheus-community](https://prometheus-community.github.io/helm-charts). `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
- From same helm repo we get statsd-exporter-0.7.0

It is probably better to install [helmfile](https://github.com/helmfile/helmfile) on your local machine and run the helmfile.yaml instead. That will make sure all the repostories and apps are installed with the right versions.

```
curl -L -o /tmp/helmfile_0.149.0_linux_amd64.tar.gz https://github.com/helmfile/helmfile/releases/download/v0.149.0/helmfile_0.149.0_linux_amd64.tar.gz \
&& tar -zxvf /tmp/helmfile_0.149.0_linux_amd64.tar.gz -C /tmp \
&& mv /tmp/helmfile /usr/local/bin/helmfile \
&& helmfile version
```

You also need to install helm and helm diff

`helm plugin install --version v3.6.0 https://github.com/databus23/helm-diff`

## Local setup for testing

Currently I am using minikube on windows 10 installed through the installer: [minikube installation page](https://minikube.sigs.k8s.io/docs/start/)

The installer will add the minikube executable to your PATH by default. Also I make use of metallb addon in minikube in order to test my application with replication and load-balancing.

For things like testing with kubectl helm and docker I am using WSL2 [example guide](https://pureinfotech.com/install-windows-subsystem-linux-2-windows-10/). For docker specifically you need to install docker desktop and enable WSL2 based engine.

### Tips and Tricks

For a smooth experience that allows me to run kubectl and minikube from WSL you need to do the following:

#### Setting up kubectl

1. After starting your minikube cluster you will find your kube config here
    ```
    more %userprofile%\.kube\config
    ```
2. Copy the config and make some adjustments to the .clusters.cluster.certificate-authority path and .users.user.client-certificate .users.user.client-key path the adjustments should follow the example below
    ```
    original:
        C:\Users\youruser\.minikube\ca.crt
    adjusted:
        /mnt/c/Users/youruser/.minikube/ca.crt
    ```
3. Paste the new config into your local kube config path inside your WSL2 environment
    ```
     vim ~/.kube/config
    ```
4. You should now be able to use kubectl commands inside WSL2 against your minikube cluster

#### Setting up minikube

1. In your WSL2 environment create a minikube file un usr local bin
    ```
    vim /usr/local/bin/minikube
    ```
2. Paste the following script into the file (assuming your minikube.exe is on that path)
    ```
    #!/bin/sh
    /mnt/c/Program\ Files/Kubernetes/Minikube/minikube.exe
    ```
3. chmod the file so that it is executable
    ```
     chmod +x /usr/local/bin/minikube
    ```
4. You should now be able to use minikube commands from within WSL2