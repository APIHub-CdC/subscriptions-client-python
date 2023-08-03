# Subscriptions-Client-Python

  

## Requirements

Python >= 3.9.16
pip
System Linux/Unix
Git

### Additional Dependencies
You MUST have installed in your system the following dependencies:

- openssl ~ 3.0.7
- python cryptography ~ 41.0.2
- python requests ~ 2.31.0

```sh
# For RHEL or derivatives:
yum install openssl
dnf install openssl

# For Debian or derivatives:
apt install openssl
```
```sh
pip install cryptography
pip install requests
```
  

## Start Guide

### Step 1. Clone the repository
Clone this repository in your Linux/Unix system.
You can use the following command:
```sh
git clone <nombre_del_repositorio>
```

### Step 2. Generate the cryptographic keys

 - Run the bash file *crypto_keys_generator.sh* from the command line in your Unix/Linux system.
 - Store in a secure vault the chosen password for the PKCS12 keystore during the execution of the file *crypto_keys_generator.sh*
 - Identify from the output of the executed file *crypto_keys_generator.sh* the directory where the generated keys were stored.

### Step 3. Download the Círculo de Crédito public certificate

 1. Go to the Círculo de Crédito Developers web site
 2. Login in the web site
 3. Upload your own public certificate and Download the Círculo de Crédito public certificate
  

### Step 4. Add your credentials to call the API

 - Identify the *ApiSubscription* class in the module *subscription-test*.
 - Edit the class adding the path of your cryptographic keys and your API credentials.
 - Edit the class adding the URL of your webhook and the credentials required to be authenticated in your webhook.

**IMPORTANT**: Your webhook MUST implement the *HTTP Basic Authentication* (RFC-7617) security mechanism.

```python
# ...
class  ApiSubscription:

def  __init__(self):
# API cryptographic keys
self.public_cert_path = "/your-file-path/cdc_cert_xxxx.pem"
self.pkcs12_path = "/your-file-path/keystore.p12"
self.pkcs12_password = "your-keystore-secure-password"

# API credentials
self.api_username = "your-username"
self.api_password = "your-password"
self.api_key = "your-api-key"
# ...
```
```python
def  create_new_subscription(self):
# ...
try:
# Subscription data
subscription = {
ApiSubscriptionsService.WEBHOOK_URL: "https://your-webhook-url",
ApiSubscriptionsService.ENROLLMENT_ID: str(uuid.uuid1()),
ApiSubscriptionsService.EVENT_TYPE: "mx.com.circulodecredito.<event-type>"
}

webhook_username = "your-secure-username"
webhook_password = "your-secure-password"
# ...
```

### Step 5. Call the API Subscriptions

Uncomment the required method to call the Subscriptions API.

```python
# ...
api_subscriptions = ApiSubscription()
#api_subscriptions.create_new_subscription()
#api_subscriptions.find_subscription()
# ...
```

Run the file subscription-test.py
```ssh
python3 subscription-test.py
```


[CONDICIONES DE USO, REPRODUCCIÓN Y DISTRIBUCIÓN](https://github.com/APIHub-CdC/licencias-cdc)

[1]: https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos