# Use the official Ubuntu base image
FROM ubuntu:22.04

# Create a directory for the app
WORKDIR /root

# Copy the .env file to the container
COPY .env .env

# Check env var
RUN echo $CLOUDFLARE_VM_SSH_ENDPOINT

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Add Cloudflare GPG key
RUN mkdir -p --mode=0755 /usr/share/keyrings \
    && curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Add Cloudflare repository to apt sources
RUN echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared jammy main' | tee /etc/apt/sources.list.d/cloudflared.list

# Update apt cache and install cloudflared
RUN apt-get update && \
    apt-get install -y --no-install-recommends cloudflared && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ~/.ssh

# Add the Cloudflare tunnel configuration file
RUN export $(cat .env | xargs) && \
    echo "Host $CLOUDFLARE_VM_SSH_ENDPOINT \n\
    ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h" > ~/.ssh/config

# Expose any ports needed by your application
# EXPOSE <port>

# Start your application
CMD ["bash", "entrypoint.sh"]