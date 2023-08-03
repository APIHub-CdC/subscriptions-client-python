"""
Copyright (C) 2023 Círculo de Crédito - All Rights Reserved

Unauthorized use, copy, modification and/or distribution 
of this software via any medium is strictly prohibited.

This software CAN ONLY be used under the terms and conditions 
established by 'Círculo de Crédito' company.

Proprietary software.
"""
import logging
import json
import base64
import traceback

from ecc_service import ECDSAService
from encryption_service import AESService

class WebhookService:
    """
    Service class with utility methods for the registration of the webhook in the API subscriptions.

    :Author: Ricardo Rubio
    :Copyright: 2023 Círculo de Crédito
    """

    def __init__(self, ecdsa_service, log):
        """
        Constructor.

        :param ecdsa_service: A service object for the usage of ECDSA cryptography.
        :type ecdsa_service: ECDSAService

        :param log: A logger object to print logs.
        :type log: logging
        """

        self.ecdsa_service  = ecdsa_service
        self.aes_service    = AESService(log)
        self.log            = log

    def generate_auth_token(self, webhook_username, webhook_password):
        """
        Generate the 'x-webhook-jwt-auth' header value for the registration of a new subscription.

        NOTE: The credentials (webhook_username and webhook_password) correspond with the authentication
        credentials that will be used by 'Círculo de Crédito' when calling the grantor webhook to send
        the asynchronous notification of any API.

        NOTE: The grantor must implement the 'Basic HTTP Authentication' security mechanism in its webhook
        as defined in the RFC 7617.

        :param webhook_username: The grantor webhook username.
        :type webhook_username: str

        :param webhook_password: The grantor webhook password.
        :type webhook_password: str 

        :return: The generated 'x-webhook-jwt-auth' value if success and empty otherwise.
        :rtype: str or None
        """

        self.log.info(f"Generating webhook jwt auth")

        encryption_key  = self.ecdsa_service.derive_ecdh_32bits_key()
        encryption_iv   = self.aes_service.generate_iv()

        webhook_credentials = {
            "username": webhook_username,
            "password": webhook_password
        }

        plain_text = json.dumps(webhook_credentials)

        encrypted_text = self.aes_service.encrypt_aes_gcm_nopadding(plain_text, encryption_iv, encryption_key)

        encryption_iv_base64 = base64.b64encode(encryption_iv).decode('utf-8')

        self.log.info(f"Webhook jwt auth generated successfully!")

        return f"{encrypted_text.hex()}.{encryption_iv_base64}"