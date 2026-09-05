# VPS setup

The VPS is the public gateway. WireGuard carries traffic between it and the
Moodle VM at home. Caddy terminates TLS and proxies through the tunnel.

This is a condensed version of [WireGuard VPS to Homelab Tunnel: Port
Forwarding + Caddy](https://diymediaserver.com/post/2026/install-wireguard-vps-homelab-tunnel/),
adapted for ufw and this project's addresses. Read that guide for background
and troubleshooting, especially the MTU section.

Addresses: the VPS is `10.0.0.1` on the tunnel, the Moodle VM is `10.0.0.2`.

## Install

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y wireguard ufw
```

## Firewall

Allow SSH before enabling ufw, or you lock yourself out. No NAT or forwarding
rules are needed: Caddy proxies, so the kernel never routes this traffic.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 51820/udp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## WireGuard

Generate the keypair and note the public key. The VM setup asks for it.

```bash
sudo chmod 700 /etc/wireguard
cd /etc/wireguard
sudo sh -c 'wg genkey | tee private.key | wg pubkey > public.key'
sudo cat public.key
```

Copy `wg0.conf.example` from this directory to `/etc/wireguard/wg0.conf` and
fill in the private key. Leave the `[Peer]` section until the VM setup prints
its public key, then fill that in too.

```bash
sudo systemctl enable --now wg-quick@wg0
```

After adding the VM's key, apply it:

```bash
sudo systemctl restart wg-quick@wg0
```

## Caddy

Install from Caddy's official apt repository:

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy
```

Copy `Caddyfile` from this directory over `/etc/caddy/Caddyfile`, then:

```bash
sudo systemctl reload caddy
```

## DNS

Add one A record at Porkbun: `moodle.alanjam.com` pointing to the VPS public
IPv4. Caddy retries its certificate until DNS resolves and the tunnel is up,
so early failures are normal.

## If large transfers stall

Pages load but uploads hang: lower the MTU. Add `MTU = 1420` to the
`[Interface]` section of `wg0.conf` on both ends and restart both interfaces.
