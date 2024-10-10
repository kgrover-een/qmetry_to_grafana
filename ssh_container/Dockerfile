# Official Ubuntu base image
FROM ubuntu:latest

# Installing OpenSSH server and sudo
RUN apt-get update && apt-get install -y openssh-server sudo

# Creating a user for SSH access without specifying a UID
RUN useradd -rm -d /home/kanika -s /bin/bash -G sudo kanika && \
    echo 'kanika:password' | chpasswd

# Allow SSH root login and adjust the sshd_config
RUN mkdir /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'AllowUsers kanika' >> /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]

