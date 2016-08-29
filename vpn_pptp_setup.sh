#!/bin/bash


#name: vpn_pptp_setup
#author: Smirnov Kirill smirnovkirilll.github.io
#revision: 2.1
#revision date: 29.08.2016
#description:
#1.this is a simple wrapper for establishing connection to corporate vpn (client and server are pre-configured!)
#2.it is supposed, that prerequisitions are performed:
#pptp package, modules are installed, some rules added to firewall
#config files (below) are tuned:
#/etc/ppp/chap-secrets
#/etc/ppp/peers/name_of_peer
#/etc/ppp/options.pptp
#3.to start-stop vpn-pptp just call script, it will detect whether you inside or outside your corporation_vpn and offer opposite action


#CONFIGS
#outter ip of corporation vpn:
corp_ip='[ip_address]'
peer_name='[peer_name]'
#initial status values
declare -A status
status=(
  [outtr_ip]=''
  [state]=''
  [action]=''
  [full_state]='' 
  )
#initial inner_status values
declare -A inner_status
inner_status=(
  [inner_ip]=''
  [ppp0_state]=''
  )
#initial error values
declare -a errors


#4.SCRIPT
#throw away from script on detected error and stop vpn
error_handler () {  
  if [[ ${errors[@]} = '' ]]; then
    echo "$(tput setaf 2)no errors detected$(tput sgr 0)"
  else
    echo "$(tput setaf 1)exiting on error: ${errors[@]}$(tput sgr 0)"
    echo "trying to stop vpn..."
    stop_vpn
    exit 1
  fi
}


check_status () {
  #using curl to check IP, time of answer limited for 5 secs
  outtr_ip=$(curl --silent --max-time 5 ipinfo.io/ip)
  #check whether its inside VPN or not
  if [[ $outtr_ip = '' ]]; then
    outtr_ip="none_ip"
    state="couldn't check state"
    action="none_action"
    errors+=("internet off")
  elif [[ $outtr_ip = $corp_ip ]]; then
    state="inside_vpn"
    action="stop_vpn"
  else
    state="outside_vpn"
    action="start_vpn"
  fi

  full_state="your outtr_ip: ${outtr_ip}, you're: ${state}"
  status=(
    [outtr_ip]=$outtr_ip
    [state]=$state
    [action]=$action
    [full_state]=$full_state 
    )
}


check_inner_status () {
  #check inner_vpn_ip, it exists only inside vpn
  inner_ip=$(ip -4 a l dev ppp0 | grep inet | awk '{ print $2 }' | cut -f 1 -d \/)
  #check if inner_vpn_ip looks like IP
  if [[ $inner_ip = *[a-z]* ]] || [[ $inner_ip = '' ]]; then
    inner_ip="none_ip"
    ppp0_state="off"
    errors+=("ppp0 does not exist")
  else
    ppp0_state="on"
  fi

  echo "inner_ip: $inner_ip, ppp0_state: $ppp0_state"
  inner_status=(
    [inner_ip]=$inner_ip
    [ppp0_state]=$ppp0_state
  )
}


start_vpn () {
  check_status
  if [[ ${status[action]} != "start_vpn" ]]; then
    errors+=("action is not start_vpn")
  fi
  error_handler
  #basic vpn call
  sudo pppd call $peer_name
  #need some time...
  sleep 5s
  check_inner_status
  error_handler
  sudo route add default gw ${inner_status[inner_ip]}
}


stop_vpn () {
  check_inner_status
  if [[ ${inner_status[ppp0_state]} = "on" ]]; then
    sudo route del default gw ${inner_status[inner_ip]}
  fi
  sudo route del $corp_ip
  sudo killall pppd
}


#MAIN BODY
#get information about current status
check_status
echo ${status[full_state]}
error_handler
read -p "do you wanna $(tput setaf 3)${status[action]}$(tput sgr 0) vpn (y/n): " user_answer
if [[ $user_answer = *('y'|'Y'|'yes') ]]; then
  ${status[action]} #calling function  (start|stop) by name, kept in variable
  #wait for chanfes to be finished 
  sleep 5s
  check_status
  echo ${status[full_state]}
  error_handler
else
  echo "no 'yes' answer received (or bad status) nothing to do, bye"
fi


exit 0