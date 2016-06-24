/interface bridge
remove [ find name=bridge1 ]
add name=hs-bridge
/interface wireless
set [ find default-name=wlan1 ] disabled=no mode=ap-bridge wireless-protocol=802.11
/ip pool
remove [ find name=dhcp ]
add name=hs-pool-default ranges=192.168.88.10-192.168.88.200
/ip dhcp-server
add address-pool=hs-pool-default disabled=no interface=hs-bridge name=hs-dhcp-default
/interface bridge port
remove [ find interface=ether2 ]
remove [ find interface=ether3 ]
remove [ find interface=ether4 ]
remove [ find interface=ether5 ]
remove [ find interface=wlan1 ]
add bridge=hs-bridge interface=ether2
add bridge=hs-bridge interface=ether3
add bridge=hs-bridge interface=ether4
add bridge=hs-bridge interface=ether5
add bridge=hs-bridge interface=wlan1
/ip address
add address=192.168.88.1/24 interface=hs-bridge network=192.168.88.0
/ip dhcp-client
add dhcp-options=hostname,clientid disabled=no interface=ether1
/ip dhcp-server network
add address=192.168.88.0/24 gateway=192.168.88.1 netmask=24
/ip dns
set allow-remote-requests=yes servers=8.8.8.8
/ip firewall nat
add action=masquerade chain=srcnat comment=hs-nat-default out-interface=ether1
/ip service
set telnet disabled=yes
set api-ssl disabled=yes
/system leds
set 5 interface=wlan1