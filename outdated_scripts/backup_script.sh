#!/bin/bash


#name: backup&encrypt
#author: Smirnov Kirill smirnovkirilll.github.io
#revision: 1.5
#revision date: 11.07.2016
#description:
#simple backup & encrypt utility
#1.checks if source, destination directory, list of being copied folders, passphrase are ok
#2.for each folder choosen too bakup checks already exist fresh copy (if it is, script will not make that work again, if its absent, than next)
#3.tar -> gpg -> moves to backup copies to destination directory
#4.for storing its good too choose folder, that plugged to remote server (dropbox, yandex.disk etc)
#5.thats it. simple script to put on cron or start manual to backup some folders
#6.to decrypt encrypted files you should:
#gpg --passphrase [passphrase] [filename]
#7.feature request: i think all parts of this script should be kept in separate functions for easier maintaining, but in some places i don't understand how to implement it


#CONFIG
dir_src="${HOME}/some_storage"
dir_dst="${HOME}/backup_storage"
folders=(
  some
  folders
  to
  be
  backed
  up )


#SCRIPT


#1.check if config is ok or not
config_error='no_errors'
if [[ ! -d $dir_src ]]; then
  config_error=$dir_src
fi
  
if [[ ! -d $dir_src ]]; then
  config_error=$dir_dst
fi
  
for folder in ${folders[@]}; do
  if [[ ! -d ${dir_src}/${folder} ]]; then
    config_error=${dir_src}/${folder}
  fi
done
  
if [[ ! $config_error = 'no_errors' ]]; then
  echo "there is no such directory '${config_error}', check your config"
  exit 1
else
  echo "config is ok"
fi


#2.findout which folders are really need to be backuped
folders_checked=()
folders_checked_no=()

for folder in ${folders[@]}; do
  dir_src_full="${dir_src}/${folder}"
  dir_dst_full="${dir_dst}/${folder}.tar.gpg"
  date_src=$(stat -c %y ${dir_src_full})
  date_dst=$(stat -c %y ${dir_dst_full})
  if [[ ${date_src} > ${date_dst} ]] || [[ ! -e ${dir_dst_full} ]]; then
    folders_checked+=(${folder})
  else
    folders_checked_no+=(${folder})
  fi
done

echo "folders to be backed up: ${folders_checked[@]}"
echo "folders exist and fresh (will not be backed up): ${folders_checked_no[@]}"


#3.read and check passphrase
passphrase=''
echo "give passphrase to encrypt backup or print 'exit'"
while [[ $passphrase = '' ]]; do
  read -s -p 'passphrase1: ' pass_candidate
  if [[ $pass_candidate = 'exit' ]]; then
    echo -e "\nok, bye"
    exit 0
  elif [[ $pass_candidate =~ ' ' ]] || [[ ${#pass_candidate} -lt 7 ]]; then
    echo -e "\nyour passphrase should not -contain spacebars, -be less than 7 chars long, try again"
  else
    echo -e "\nrepeat passphrase"
    read -s -p 'passphrase2: ' pass_candidate2
    if [[ $pass_candidate != $pass_candidate2 ]]; then
      echo -e "\npassphrases not equal, try again"
    else
      passphrase=$pass_candidate
      echo -e "\npassphrase accepted..."
    fi
  fi
done


#4.backup folders needed, encrypt, rm temp tars, move gpg to its dst dir
for folder in ${folders_checked[@]}; do
  tar -cvzf ${dir_src}/${folder}.tar ${dir_src}/${folder}
  gpg --passphrase $passphrase -c ${dir_src}/${folder}.tar
  rm ${dir_src}/${folder}.tar
  mv ${dir_src}/${folder}.tar.gpg ${dir_dst}/${folder}.tar.gpg
done


echo "all done, now your backup destination folder contains:"
ls -la $dir_dst
exit 0
