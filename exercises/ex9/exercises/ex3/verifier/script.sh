#!/bin/sh

echo "Starting verifier..."

if [ -f /current_dir/request.csr ]; then
    echo "Found file request.csr, going to sign it with CA key"
    rm -f /current_dir/request.crt 
    openssl x509 -req -in /current_dir/request.csr -CA /app/rootCA.pem -CAkey /app/rootCA.key -CAcreateserial -out /current_dir/request.crt -days 5000 -sha256

    echo "Done"
    ls /current_dir
else
    echo "File request.csr not found, skipping CA signature... (restart the image to re-run this test). Content of the current directory:"
    ls /current_dir
fi

echo ""
echo "Continuing with the test..."
echo ""

python3 verifier.py