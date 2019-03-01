file: /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US
     
network={
    ssid="YOURSSID"
    psk="YOURPASSWORD"
    scan_ssid=1
}

# run sudo wpa_cli -i wlan0 reconfigure