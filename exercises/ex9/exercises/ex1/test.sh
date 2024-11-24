#!/bin/sh

cleanup() {
    docker compose down --remove-orphans
}
trap cleanup SIGINT

build() {
    docker compose build
    docker compose up -d
    sleep 5
}

print_ip() {
    echo "Client IP"
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client

    echo "Mitm IP"
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mitm
}

set_iptables() {
    # get MITM's IP
    MITM_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mitm | head -n 1)

    # set client's default gateway to MITM's IP
    docker compose exec client route del default
    docker compose exec client route add default gateway ${MITM_IP} eth0
    docker compose exec client route

    # make sure forwarding is 1 in MITM
    docker compose exec mitm sysctl net.ipv4.ip_forward

    # enable NAT in MITM
    docker compose exec mitm iptables -A FORWARD -i eth0 -j ACCEPT
    docker compose exec mitm iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

    # stop forwarding, dump in NFQUEUE 0
    docker compose exec mitm iptables -D FORWARD -i eth0 -j ACCEPT
    docker compose exec mitm iptables -A FORWARD -j NFQUEUE --queue-num 0
}

build
print_ip
set_iptables

rm -f test.log

echo "Starting test for 30 seconds..."
timeout 30 docker exec mitm python3 /app/mitm.py | tee test.log

if [ $(cat test.log | grep "New secret found" | wc -l) -eq 0 ]; then
    echo "Test failure !";
    cleanup
    exit 1;
fi

rm -f test.log

cleanup
echo "Test succeeded."
exit 0
