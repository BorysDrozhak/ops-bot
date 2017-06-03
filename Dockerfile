FROM frolvlad/alpine-python3:latest



RUN pip3 install --upgrade pip

RUN pip3 install pytelegrambotapi
RUN pip install toml
RUN pip install boto

RUN apk add --update make
RUN apk add --update ansible
RUN apk add --update bash git curl wget

RUN pip install ansible

RUN wget -q https://releases.hashicorp.com/terraform/0.8.6/terraform_0.8.6_linux_amd64.zip \
  -O /terraform.zip ; \
  unzip /terraform.zip -d /usr/bin/ ; \
  rm -f /terraform.zip



COPY src/ /opt/

CMD [ "python3", "./opt/bot.py" ]   