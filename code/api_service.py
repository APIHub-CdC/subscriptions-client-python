"""
Copyright (C) 2023 Círculo de Crédito - All Rights Reserved

Unauthorized use, copy, modification and/or distribution 
of this software via any medium is strictly prohibited.

This software CAN ONLY be used under the terms and conditions 
established by 'Círculo de Crédito' company.

Proprietary software.
"""
import requests
import json
import logging
import traceback

from ecc_service import ECDSAService

class ApiSubscriptionsService:
    """
    Class service to call the Subscriptions API of 'Círculo de Crédito'.

    :Author: Ricardo Rubio
    :Copyright: 2023 Círculo de Crédito
    """

    API_URL         = "https://services.circulodecredito.com.mx/v1/subscriptions"
    
    USERNAME        = "username"
    PASSWORD        = "password"
    X_API_KEY       = "x-api-key"
    X_SIGNATURE     = "x-signature"
    X_WEB_AUTH      = "x-webhook-jwt-auth"
    
    WEBHOOK_URL     = "webHookUrl"
    ENROLLMENT_ID   = "enrollmentId"
    EVENT_TYPE      = "eventType"

    def __init__(self, api_username, api_password, api_key, ecdsa_service, log):
        """
        Constructor.

        :param api_username: The assigned username for the consumption of the 'Círculo de Crédito' APIs.
        :type api_username: str

        :param api_password: The assigned password for the consumption of the 'Círculo de Crédito' APIs.
        :type api_password: str

        :param api_key: The assigned key for the consumption of the 'Círculo de Crédito' APIs.
        :type api_key: str

        :param ecdsa_service: A service object to perform cryptographic functionality.
        :type ecdsa_service: ECDSAService

        :param log: A logger object to print logs.
        :type log: logging
        """
        
        self.api_username   = api_username
        self.api_password   = api_password
        self.api_key        = api_key
        self.ecdsa_service  = ecdsa_service
        self.log            = log

    def createSubscription(self, x_webhook_auth, subscription):
        """
        Call the Subscriptions API to create a new subscription and register a webhook URL to receive
        asynchronous API notifications for the specified event type.

        :param x_webhook_auth: The webhook credentials encrypted as specified by the Subscriptions API.
        :type x_webhook_auth: str

        :param subscription: The request body that will be send when calling the subscriptions API.
        :type subscription: dict

        :return: If success, the HTTP response object of the API call is returned.
        :rtype: requests.Response
        """
        
        self.log.info("Starting x-signature generation")

        signature = self.ecdsa_service.sign_ecdsa_sha256(json.dumps(subscription))

        self.log.info(f"x-signature: {signature.hex()}")
        self.log.info(f"x-webhook-jwt-auth: {x_webhook_auth}")

        headers = {
            self.USERNAME: self.api_username,
            self.PASSWORD: self.api_password,
            self.X_API_KEY: self.api_key,
            self.X_SIGNATURE: signature.hex(),
            self.X_WEB_AUTH: x_webhook_auth 
        }

        self.log.info("Calling API subscriptions - Create new subscription")

        response = requests.post(self.API_URL, headers=headers, json=subscription)

        self.log.info(f"API Subscriptions Response Status: {response.reason} {response.status_code}")

        return response

    def find_subscription_by_id(self, subscription_id):
        """
        Call the Subscriptions API to find the specified subscription by id.

        :param subscription_id: The unique identifier of the subscription that will be searched.
        :type subscription_id: str

        :return: If success, the HTTP response object of the API call is returned.
        :rtype: requests.Response
        """

        url = self.API_URL + f"/{subscription_id}"

        self.log.info("Starting x-signature generation")

        signature = self.ecdsa_service.sign_ecdsa_sha256(url)

        self.log.info(f"x-signature: {signature.hex()}")

        headers = {
            self.USERNAME: self.api_username,
            self.PASSWORD: self.api_password,
            self.X_API_KEY: self.api_key,
            self.X_SIGNATURE: signature.hex()
        }

        self.log.info("Calling API subscriptions - find subscription by Id")

        response = requests.get(url, headers=headers)

        self.log.info(f"API Subscriptions Response Status: {response.reason} {response.status_code}")

        return response


