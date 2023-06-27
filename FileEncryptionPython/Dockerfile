FROM python
RUN apt install -y && apt update -y && apt upgrade -y && apt dist-upgrade -y
COPY app /app
WORKDIR /app
RUN apt install swig -y
RUN pip3 install -r request.txt
RUN mkdir -p /opt/procrypt/km3000/config/
COPY config /opt/procrypt/km3000/config/
COPY libhsm.so /lib/
COPY libhsm.so /lib64/
COPY HSM.so /lib64/
# Değişken tanımlama
ENV HSM_SO_FILE=/lib64/HSM.so
ENTRYPOINT [ "python3","app.py" ]
