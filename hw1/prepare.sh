#!/usr/bin/env bash
set -euo pipefail

HOSTS=(192.168.1.35 192.168.1.36 192.168.1.37)
USER="team"
KEY="$HOME/.ssh/id_rsa"
PUBKEY="$KEY.pub"

# Install Ansible and sshpass
if ! command -v ansible >/dev/null 2>&1; then
  echo "Installing Ansible and sshpass..."
  sudo apt-get update
  sudo apt-get install -y ansible sshpass
else
  echo "Ansible is already installed."
fi

# Generate SSH key if missing
[[ -f "$KEY" && -f "$PUBKEY" ]] || ssh-keygen -t rsa -b 4096 -N '' -f "$KEY"

# Read password once
read -rs -p "Password for ${USER}@remote hosts: " PASS
echo

# Copy SSH keys
for H in "${HOSTS[@]}"; do
  sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$USER@$H" "mkdir -p ~/.ssh && chmod 700 ~/.ssh || true"
  if ! sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$USER@$H" "grep -qxF '$(cat $PUBKEY)' ~/.ssh/authorized_keys 2>/dev/null"; then
    sshpass -p "$PASS" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$PUBKEY" "$USER@$H":/tmp/id_rsa_pub.$$
    sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$USER@$H" \
      "cat /tmp/id_rsa_pub.$$ >> ~/.ssh/authorized_keys && rm -f /tmp/id_rsa_pub.$$ && chmod 600 ~/.ssh/authorized_keys"
    echo "Key installed on $H"
  else
    echo "Key already exists on $H"
  fi
done

echo "SSH access configured, Ansible installed."

