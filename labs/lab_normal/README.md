######## EXECUTE THE LAB #####################
************
1  Go to the folder where the docker-compose is located

2  Enter the credentials of an email in the **generator/generate-traffic/mailing/mail.ini** file that will be used to generate email traffic.


```
[mailconfig]
user = mail@example.com
pw = password
smtp = smtp.gmail.com
```


3  Execute **docker-compose build**

4  Execute: **docker-compose up --abort-on-container-exit**

5  Run when you want to extract the traffic generated in CICFlowMeter and Netflow format: **docker-compose exec router ./getCIC.sh**