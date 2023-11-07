# I. Simple bs program

## 1. First steps

🌞 **`bs_server_I1.py`**

[TP4 repo](https://github.com/Elyter/tp4-dev)

🌞 **`bs_client_I1.py`**

[TP4 repo](https://github.com/Elyter/tp4-dev)

🌞 **Commandes...**

**Serveur**
```
[elyter@serveur ~]$ git clone https://github.com/Elyter/tp4-dev

[elyter@serveur ~]$ cd tp4-dev/

[elyter@serveur tp4-dev]$ sudo firewall-cmd --add-port=13337/udp --permanent
success

[elyter@serveur tp4-dev]$ sudo firewall-cmd --add-port=13337/tcp --permanent
success

[elyter@serveur tp4-dev]$ sudo firewall-cmd --reload
success

[elyter@serveur tp4-dev]$ python bs_server_I1.py 
Connected by ('10.37.128.4', 36966)
Données reçues du client : b'Meooooo !'

[elyter@serveur tp4-dev]$ ss -nla | grep 13337
tcp   LISTEN 0      1   
```
**Client**
```
[elyter@client ~]$ git clone https://github.com/Elyter/tp4-dev

[elyter@client ~]$ cd tp4-dev/

[elyter@client tp4-dev]$ python bs_client_I1.py
Le serveur a répondu b'Hi mate !'
```


## 2. User friendly

🌞 **`bs_client_I2.py`**

[TP4 repo](https://github.com/Elyter/tp4-dev)

🌞 **`bs_server_I2.py`**

[TP4 repo](https://github.com/Elyter/tp4-dev)

## 3. You say client I hear control


🌞 **`bs_client_I3.py`**

[TP4 repo](https://github.com/Elyter/tp4-dev)