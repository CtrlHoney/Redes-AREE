#!/bin/sh
set -e

if [ -z "$ip" ]; then
    echo "A variável ip não está definida!"
    exit 1
fi

ip route del default && ip route add default via $ip && python main.py