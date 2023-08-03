# Subscriptions-Client-Python

  

## Requisitos

Python >= 3.9.16
Sistema Linux/Unix
Git

### Dependencias adicionales

Se debe contar con las siguientes dependencias:
- openssl ~ 3.0.7
- python cryptography ~ 41.0.2
- python requests ~ 2.31.0

```sh
# Para RHEL o derivados:
yum install openssl
dnf install openssl

# Para Debian o derivados:
apt install openssl
```
```sh
pip install cryptography
pip install requests
```
  

## Guía de inicio

### Paso 1. Clonar repositorio
Clona este repositorio en tu sistema Linux/Unix
Utiliza el siguiente comando:
```sh
git clone <nombre_del_repositorio>
```

### Paso 2. Generar llaves criptográficas

 - Ejecuta el archivo *crypto_keys_generator.sh* desde la línea de comandos de su sistema Unix/Linux
 - Resguardar en una bóveda segura la contraseña elegida para el keystore durante la ejecución del archivo *crypto_keys_generator.sh*
 - Identifica el directorio generado donde se guardaron las llaves generadas

### Paso 3. Descarga el certificado público de Círculo de Crédito

 1. Ingresa al portal de desarrolladores
 2. Inicia sesión en el portal
 3. Descarga el certificado

  

### Paso 4. Agrega tus credenciales para poder invocar el API

 - Identifica la clase *ApiSubscription* en el módulo *subscription-test*.
 - Edita la clase agregando la ruta de los archivos con las llaves criptográficas así como tus credenciales para consumir el API .
 - Edita la clase y agrega la URL de tu webhook así como las credenciales (usuario y contraseña) con las que se encuentra protegido el acceso a tu webhook.

**IMPORTANTE**: Tu webhook debe utilizar el mecanismo de seguridad *HTTP Basic Authentication*.

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

### Paso 5. Consumir el API Subscriptions

Descomenta el método correspondiente para llamar el API y crear una nueva subscription o encontrar una existente.

```python
# ...
api_subscriptions = ApiSubscription()
#api_subscriptions.create_new_subscription()
#api_subscriptions.find_subscription()
# ...
```

Ejecuta el archivo subscription-test.py
```ssh
python3 subscription-test.py
```


[CONDICIONES DE USO, REPRODUCCIÓN Y DISTRIBUCIÓN](https://github.com/APIHub-CdC/licencias-cdc)

[1]: https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos