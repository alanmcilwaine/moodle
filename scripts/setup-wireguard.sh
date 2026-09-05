#!/usr/bin/env bash
# Configure the WireGuard tunnel to the VPS. Run once, with sudo, before
# just setup. Prints the public key to add to the VPS.
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "Run with sudo: sudo ./scripts/setup-wireguard.sh <VPS public IP>" >&2
    exit 1
fi

if [[ $# -ne 1 ]]; then
    echo "Usage: sudo ./scripts/setup-wireguard.sh <VPS public IP>" >&2
    exit 1
fi
vps_ip="$1"

apt-get update -qq
apt-get install -y -qq wireguard

if [[ ! -f /etc/wireguard/private.key ]]; then
    (umask 077 && wg genkey | tee /etc/wireguard/private.key | wg pubkey > /etc/wireguard/public.key)
fi

read -rp "VPS WireGuard public key: " vps_public_key

cat > /etc/wireguard/wg0.conf <<EOF
[Interface]
Address = 10.0.0.2/24
PrivateKey = $(cat /etc/wireguard/private.key)

[Peer]
# VPS
PublicKey = ${vps_public_key}
Endpoint = ${vps_ip}:51820
AllowedIPs = 10.0.0.1/32
PersistentKeepalive = 25
EOF
chmod 600 /etc/wireguard/wg0.conf

systemctl enable --now wg-quick@wg0

echo "WireGuard is up. Add this public key to the [Peer] section of /etc/wireguard/wg0.conf on the VPS:"
cat /etc/wireguard/public.key
echo "Then run on the VPS: sudo systemctl restart wg-quick@wg0"
