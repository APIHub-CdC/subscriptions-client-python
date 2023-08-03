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

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AESService:
    """
    Service class that provide AES encryption functionality.

    :Author: Ricardo Rubio
    :Copyright: 2023 Círculo de Crédito
    """

    def __init__(self, log):
        """
        Constructor.

        :param log: A logger object to print logs.
        :type log: logging
        """
        self.log = log

    def generate_iv(self):
        """
        Generate a pseudo-random IV value of 16 bits for AES encryption.
        """
        self.log.info("Generating pseudo-random IV for AES encryption")
        return os.urandom(16)

    def encrypt_aes_gcm_nopadding(self, plain_text, iv, key):
        """
        Encrypt the plaint text provided as argument using the encryption iv and key arguments.
        The encryption use the AES-256 algorithm with GCM and no padding.

        :param plain_text: The data that will be encrypted.
        :type plain_text: str

        :param iv: The IV for encryption.
        :type iv: bytes

        :param key: The encryption key.
        :type key: bytes

        :return: The encrypted data if the encryption is successful and empty value otherwise.
        :rtype: bytes or None
        """

        self.log.info("Encrypting with AES-256 GCM")

        try:
            aes_gcm = AESGCM(key)
            
            encrypted_text = aes_gcm.encrypt(iv, plain_text.encode('utf-8'), None)

            self.log.info("Encrypted with AES-256 GCM successfully!")

            return encrypted_text
        
        except Exception as exception:
            self.log.error(
                "Failed to encrypt the provided plain_text with AES-256-GCM no padding "
                + f"using the provided iv and key. Cause: {exception}"
            )
            traceback.print_exc()

            return None