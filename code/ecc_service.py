"""
Copyright (C) 2023 Círculo de Crédito - All Rights Reserved

Unauthorized use, copy, modification and/or distribution 
of this software via any medium is strictly prohibited.

This software CAN ONLY be used under the terms and conditions 
established by 'Círculo de Crédito' company.

Proprietary software.
"""
import os
import logging
import traceback

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import pkcs12

class ECDSAService:
    """
    Service class that provide ECDSA cryptographic functionality.

    :Author: Ricardo Rubio
    :Copyright: 2023 Círculo de Crédito
    """

    def __init__(self, public_cert_path, pkcs12_path, pkcs12_password, log):
        """
        Constructor.

        :param public_cert_path: The full file system path of the public certificate of 'Círculo de Crédito' in PEM format
        :type public_cert_path: str

        :param pkcs12_path: The full file system path of the PKCS12 file with the private key of the grantor.
        :type pkcs12_path: str

        :param pkcs12_password: The password of the PKCS12 keystore.
        :type pkcs12_password: str

        :param log: A logger object to print logs.
        :type log: logging
        """

        self.log            = log
        self.public_key     = self.load_public_key_from_certificate(public_cert_path)
        self.private_key    = self.load_private_key_from_pkcs12(pkcs12_path, pkcs12_password)

    def load_public_key_from_certificate(self, public_cert_path):
        """
        Loads an EC public key from the public certificate file in PEM format provided as argument.

        :param public_cert_path: The full file system path of the public certificate.
        :type public_cert_path: str

        :return: If success, the public key extracted from the provided public certificate is returned.
        :rtype: bytes or None
        """
        try:
            self.log.info(f"Loading public key from public certificate: {public_cert_path}")

            with open(public_cert_path, "rb") as cert_file:
                cert = x509.load_pem_x509_certificate(cert_file.read())

            self.log.info(f"Public key loaded successfully!")

            return cert.public_key()
        
        except Exception as exception:
            self.log.error(
                "Failed to load ECDSA Public Key from Public Certificate: "
                + f"{public_cert_path}. Cause: {exception}"
            )
            traceback.print_exc()

            return None

    def load_private_key(self, private_key_path, password = None):
        """
        Loads an EC private key from the provided private key file in PEM format provided as argument.

        :param private_key_path: The full file system path of the private key file.
        :type private_key_path: str

        :param password: The protection password of the private key if any.
        :type password: str

        :return: If success, the private key extracted from the file is returned.
        :rtype: bytes or None
        """
        try:
            self.log.info(f"Loading private key from: {private_key_path}")

            with open(private_key_path, "rb") as private_key_file:
                private_key = serialization.load_pem_private_key(private_key_file.read(), password)

            self.log.info("Private key loaded successfully!")

            return private_key

        except Exception as exception:
            self.log.error(f"Failed to load ECDSA Private Key: {private_key_path}. Cause: {exception}")
            traceback.print_exc()

            return None

    def load_private_key_from_pkcs12(self, pkcs12_path, pkcs12_password):
        """
        Loads an EC private key from the provided PKCS12 keystore file provided as argument.

        :param pkcs12_path: The full file system path of the PKCS12 keystore file.
        :type pkcs12_path: str

        :param password: The protection password of PKCS12 keystore.
        :type password: str

        :return: If success, the private key extracted from the file is returned.
        :rtype: bytes or None
        """
        try:
            self.log.info(f"Loading private key from PKCS12 keystore: {pkcs12_path}")

            with open(pkcs12_path, "rb") as pkcs12_file:
                private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                    pkcs12_file.read(),
                    password = pkcs12_password.encode('utf-8'),
                    backend = default_backend()
                )
            
            self.log.info("Private key loaded successfully!")

            return private_key

        except Exception as exception:
            self.log.error(f"Failed to load ECDSA Private Key from PKCS12 keystore: {pkcs12_path}. Cause: {exception}")
            traceback.print_exc()

            return None

    def derive_ecdh_32bits_key(self, private_key = None, public_key = None):
        """
        Compute a derived ECDH cryptographic key from the private and public key provided as arguments.

        NOTE: The public key provided MUST NOT be the public key associated with the private key.

        :param private_key: The EC private key that will be used to derive the ECDH key.
        :type private_key: bytes

        :param public_key: The EC public key that will be used to derive the ECDH key.
        :type public_key: bytes

        :return: If success, the derived ECDH cryptographic key is returned.
        :rtype: bytes or None
        """

        self.log.info("Deriving ECDH 32 bits secret key from private and public keys")

        if (private_key is None):
            private_key = self.private_key

        if (public_key is None):
            public_key = self.public_key

        try:
            derived_key = private_key.exchange(ec.ECDH(), public_key)

            shared_secret_key = derived_key.ljust(32, b'\0')[:32]

            self.log.info(f"ECDH 32 bits secret key derived successfully")

            return shared_secret_key

        except Exception as exception:
            self.log.error(f"Failed to derive an ECDH 32 bits key with the provided arguments. Cause: {exception}")
            traceback.print_exc()

            return None

    def sign_ecdsa_sha256(self, plain_text, private_key = None):
        """
        Compute a digital signature using the ECDSA-SH256 algorithm.

        :param plain_text: The data that will be signed.
        :type plain_text: str

        :param private_key: The EC private key that will be used to generate the signature.
        :type private_key: bytes

        :return: If success, the computed digital signature is returned.
        :rtype: bytes
        """

        self.log.info("Signing data with ECDSA-SHA265 using private key")

        if (private_key is None):
            private_key = self.private_key

        try:
            text_bytes = str.encode(plain_text, "utf-8")

            signature = private_key.sign(text_bytes, ec.ECDSA(hashes.SHA256()))

            self.log.info("Data signed sucessfully with ECDSA-SHA265")

            return signature

        except Exception as exception:
            self.log.error(f"Failed to sign the provided plain_text with the provided private key. Cause: {exception}")
            traceback.print_exc()
            
            return None

