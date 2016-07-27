/interface bridge
remove [ find name=bridge1 ]
add name=hs-bridge
/interface wireless
set [ find default-name=wlan1 ] disabled=no mode=ap-bridge wireless-protocol=802.11
/ip pool
remove [ find name=dhcp ]
add name=hs-pool-default ranges=192.168.88.10-192.168.88.200
foreach i in [/interface bridge port print ] do=[ remove $i ]
foreach i in [/interface ethernet print where name != "ether1"] do=[ /interface bridge port add interface=$i bridge=hs-bridge ]
/ip address
add address=192.168.88.1/24 interface=hs-bridge network=192.168.88.0
/ip dhcp-client
add dhcp-options=hostname,clientid disabled=no interface=ether1
/ip dhcp-server network
add address=192.168.88.0/24 gateway=192.168.88.1 netmask=24
/ip dhcp-server
add address-pool=hs-pool-default disabled=no interface=hs-bridge name=hs-dhcp-default
/ip dns
set allow-remote-requests=yes servers=8.8.8.8
/ip firewall nat
add action=masquerade chain=srcnat comment=hs-nat-default out-interface=ether1
/ip service
set telnet disabled=yes
set api-ssl disabled=yes
/system leds
set 5 interface=wlan1
