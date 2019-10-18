FROM registry.cn-shenzhen.aliyuncs.com/k8s-kubeadm/python:v3.7.3

    RUN pip install django==2.1.2 && \
    pip install djangorestframework && \
    mkdir -p /apps/working

ADD gateway /apps/working
COPY ./entrypoint.sh /apps/working

RUN chmod +x /apps/working/entrypoint.sh

WORKDIR /apps/working
ENTRYPOINT ["/apps/working/entrypoint.sh"]

CMD ["0.0.0.0:8000"]