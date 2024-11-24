#!/bin/sh
SERVER="epfl.ch"

while true
do
    echo "Testing internet connection..."

    # if not reachable, try again
    wget $SERVER -O - 1>/dev/null 2>&1

    if [ $? -eq 0 ]; then

        echo "Performing handshake..."
        ciphers=$(nmap --script ssl-enum-ciphers -p 443 $SERVER)
        hasStrongestCipher=$(echo "$ciphers" | grep 'TLS_RSA_WITH_AES_256_CBC_SHA' | wc -l)

        echo "Available ciphers:"
        nmap --script ssl-enum-ciphers -p 443 $SERVER

        if [ "$hasStrongestCipher" -eq "1" ]; then
            echo "Using stronger cipher suite (AES 256)...              <- your downgrade attack failed !"
            echo "Exchanging secret stuff on this very secure channel..."
            echo "Done."
        else
            echo "Using weaker cipher suite (AES 128)..."
            echo "Success!"

            sleep 10d # exit 0 messes up the tests
        fi
    else
        echo "Server unreachable, retrying soon..."
    fi
    sleep 10
done
