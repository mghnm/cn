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