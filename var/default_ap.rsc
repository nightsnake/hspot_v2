/ip dns
set servers=$gw allow-remote-requests=yes
/snmp
set enabled=yes
/ip service
set telnet address="" disabled=yes port=23
set ftp address="" disabled=yes port=21
set www address="" disabled=no port=80
set ssh address="" disabled=no port=22
set www-ssl address="" disabled=yes port=443
set api address="" disabled=no port=8728
set winbox address="" disabled=no port=8291
set api-ssl address="" disabled=yes port=8729
/system identity
set name=$name
/system clock
set time-zone-autodetect=no time-zone-name=Europe/Moscow
/interface bridge
remove [ find name=bridge1 ]
add name=$bridge_if
/interface wireless
set [ find default-name=wlan1 ] disabled=no mode=ap-bridge wireless-protocol=802.11 name=$wlan_if
/ip pool
remove [ find name=dhcp ]
foreach i in [/interface bridge port print ] do=[ remove $i ]
/interface bridge port add interface=ether1
/interface bridge port add interface=$wlan_if
/ip address
add address=$ip interface=$bridge_if
/ip route
add distance=1 gateway=$gw
/ip dns
set allow-remote-requests=no servers=$gw
/ip service
set telnet disabled=yes
set api-ssl disabled=yes
/system ntp client
set enabled=yes primary-ntp=$gw
/snmp community
set [ find default=yes ] addresses=$gw name=$project
/user set [ find name=admin ] password=$password
