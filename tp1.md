# TP1 : Maîtrise réseau du poste

# I. Basics

> Tout est à faire en ligne de commande, sauf si précision contraire.

☀️ **Carte réseau WiFi**

```
❯ ifconfig
en0:
	ether 80:65:7c:e1:98:31
	inet 10.33.76.201 netmask 0xfffff000 

❯ ipconfig getoption en0 subnet_mask
255.255.240.0
```

---

☀️ **Déso pas déso**

```
Lan: 10.33.64.0
Broadcast: 10.33.79.255
IP dispo: 4094
```
---

☀️ **Hostname**
```
❯ hostname
MacBook-Eliott.local
```
---

☀️ **Passerelle du réseau**
```
❯ route -n get default | grep gateway
    gateway: 10.33.79.254

❯ arp -a | grep 10.33.79.254
? (10.33.79.254) at 7c:5a:1c:d3:d8:76 on en0 ifscope [ethernet]
```
---

☀️ **Serveur DHCP et DNS**

```
❯ ipconfig getpacket en0 | grep server_identifier
server_identifier (ip): 10.33.79.254

❯ ipconfig getpacket en0 | grep domain_name_server
domain_name_server (ip_mult): {8.8.8.8, 1.1.1.1}
```
---

☀️ **Table de routage**
```
❯ netstat -nr | grep default
default            10.33.79.254       UGScg                 en0
```
---

# II. Go further


☀️ **Hosts ?**

```
❯ sudo nano /etc/hosts

1.1.1.1         b2.hello.vous
```
```
❯ ping b2.hello.vous
PING b2.hello.vous (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=38.856 ms
64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=17.692 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=57 time=22.021 ms
```
---

```
❯ lsof -i tcp | grep "ESTABLISHED" | grep  "Arc"

Arc        1064 eliott  145u  IPv6 0xafbb174f68397179      0t0  TCP 10.33.76.201:51012->par10s41-in-f10.1e100.net:443 (ESTABLISHED)

❯ ping par10s41-in-f10.1e100.net
PING par10s41-in-f10.1e100.net (142.250.75.234): 56 data bytes
64 bytes from 142.250.75.234: icmp_seq=0 ttl=117 time=39.381 ms
64 bytes from 142.250.75.234: icmp_seq=1 ttl=117 time=38.610 ms
```
---

☀️ **Requêtes DNS**

```
❯ dig +short www.ynov.com
104.26.10.233
172.67.74.226
104.26.11.233
```

```
❯ nslookup 174.43.238.89
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
89.238.43.174.in-addr.arpa	name = 89.sub-174-43-238.myvzw.com.
```

---

☀️ **Hop hop hop**

```
❯ traceroute www.ynov.com

traceroute: Warning: www.ynov.com has multiple addresses; using 104.26.10.233
traceroute to www.ynov.com (104.26.10.233), 64 hops max, 52 byte packets
 1  10.33.79.254 (10.33.79.254)  5.274 ms  3.579 ms  3.399 ms
 2  145.117.7.195.rev.sfr.net (195.7.117.145)  32.571 ms  176.437 ms  5.467 ms
```

---

☀️ **IP publique**

```
❯ curl ifconfig.me
195.7.117.146
```

---

☀️ **Scan réseau**

```
❯ netstat -an | grep ESTABLISHED | wc -l

      26
```

# III. Le requin


☀️ **Capture ARP**

[Lien vers capture ARP](./captures/arp.pcapng)

Filtre utilisé : ARP

---

☀️ **Capture DNS**

[Lien vers capture ARP](./captures/dns.pcapng)

Filtre utilisé: DNS

---

☀️ **Capture TCP**

[Lien vers capture ARP](./captures/tcp.pcapng)

---
