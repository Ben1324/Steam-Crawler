FROM python:3.9

ENV STEAM_ID=394360 
# Hearts of Iron IV

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY file_organizer.py /tmp/
COPY steam_reviews.py /tmp/
COPY client_secrets.json /tmp/
COPY pushpydrive.py /tmp/
COPY creds.txt /tmp/

COPY start.sh /tmp/
CMD ["/tmp/start.sh"]
ENTRYPOINT [ "/bin/bash" ]