#!/bin/bash


#name: vpn_pptp_setup
#author: Smirnov Kirill smirnovkirilll.github.io
#revision: 1.3
#revision date: 17.05.2016
#description:
#1.this script supposed to implement usage of functions
#2.it is a simple wrapper for establishing connection corporate vpn (client and server are pre-configured!)
#3.it is supposed, that prerequisitions are performed:
#pptp package, modules are installed, some rules added to firewall
#config files (below) are tuned:
#/etc/ppp/chap-secrets
#/etc/ppp/peers/name_of_peer
#/etc/ppp/options.pptp
#4.to start-stop vpn-pptp just call script, it will detect whether you inside or outside your corporation_vpn and offer opposite action


#CONFIGS
#outter ip of corporation vpn:
corp_ip='[ip_address]'
peer_name='[peer_name]'


#SCRIPT

check_outtr_ip () {
  outtr_ip=$(curl --silent ipinfo.io/ip)
  echo ${outtr_ip}
}

check_state () {
  if [[ $(check_outtr_ip) = $corp_ip ]]; then
    state="inside_vpn"
  else
    state="outside_vpn"
  fi
  echo ${state}
}

check_opposite_action () {
  if [[ $(check_state) = "outside_vpn" ]]; then
    action="start"
  else
    action="stop"
  fi
    echo ${action}
}

say_status () {
  echo "you're $(check_state), your outtr_ip: $(check_outtr_ip)"
}

check_inner_ip () {
  inner_vpn_ip=$(ip -4 a l dev ppp0 | grep inet | awk '{ print $2 }' | cut -f 1 -d \/)
  #check if inner_vpn_ip looks like IP
  if [[ $inner_vpn_ip = *[a-z]* ]]; then
    echo "seems like ppp0 is off: ${inner_vpn_ip}"
  else
    echo ${inner_vpn_ip}
  fi
}

start_vpn () {
  #basic vpn call
  sudo pppd call $peer_name
  #need some time...
  sleep 5s
  #add iptables rule
  sudo route add default gw $(check_inner_ip)
  #wait for getting new outter ip...
  sleep 5s
  say_status
}

stop_vpn () {
  #add iptables rule
  sudo route del default gw $(check_inner_ip)
  sudo killall pppd
  #need some time...
  sleep 5s
  say_status
}


say_status
opposite_action=$(check_opposite_action)
read -p "do you wanna ${opposite_action} vpn (y/n): " answer
if [[ $answer = *('y'|'Y'|'yes') ]] && [[ $opposite_action = "start" ]]; then
  start_vpn
elif [[ $answer = *('y'|'Y'|'yes') ]] && [[ $opposite_action = "stop" ]]; then
  stop_vpn
else
  echo "no 'yes' answer received (or bad status) nothing to do, bye"
fi

exit 0