1. [Install termux](https://f-droid.org/en/packages/com.termux/) on your device running the ISP(Internet Service Provider) you want to collect data for.
2. Now install and update some required packages
```
pkg install tsu
pkg install openssh
pkg install git
pkg install traceroute

pkg install python
pkg install python-numpy
pip install requests
pip install openpyxl

pkg update
pkg upgrade
```

3. Set up an SSH key for your termux terminal(SKIP if you already have one)
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

```
Replace "your_email@example.com" with your email address

4. View the key and copy it
```
cat ~/.ssh/id_rsa.pub
```
Copy the entire content of the public key to your clipboard.

5. Add SSH Key to Your GitHub Account (Or Other Git Hosts):
If you're using GitHub or another Git hosting service, log in to your account and navigate to your account settings. Look for the SSH key settings, often labeled "SSH and GPG keys" or similar.

    a. Click "New SSH key" or equivalent.</br>
    b. Paste your public key into the key field.</br>
    c. Give your SSH key a meaningful title (e.g., "My Laptop SSH Key").</br>
    d. Save your new SSH key.</br>
