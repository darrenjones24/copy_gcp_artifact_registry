FROM google/cloud-sdk:latest

RUN curl -L https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz -o go-containerregistry.tar.gz \ 
    && tar -zxvf go-containerregistry.tar.gz \
    && chmod +x gcrane \
    && mv gcrane /usr/local/bin/ \
    && apt install -y vim
