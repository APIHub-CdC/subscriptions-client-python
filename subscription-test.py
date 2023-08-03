"""
Copyright (C) 2023 Círculo de Crédito - All Rights Reserved

Unauthorized use, copy, modification and/or distribution 
of this software via any medium is strictly prohibited.

This software CAN ONLY be used under the terms and conditions 
established by 'Círculo de Crédito' company.

Proprietary software.
"""
import sys
import logging
import uuid
import traceback

sys.path.append('./code')

from api_service import ApiSubscriptionsService
from ecc_service import ECDSAService
from webhook_service import WebhookService

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)d - %(message)s')
log = logging.getLogger()

class ApiSubscription:

    def __init__(self):
        # API cryptographic keys
        self.public_cert_path    = "/your-file-path/cdc_cert_xxxx.pem"
        self.pkcs12_path         = "/your-file-path/keystore.p12"
        self.pkcs12_password     = "your-keystore-secure-password"

        # API credentials
        self.api_username    = "your-username"
        self.api_password    = "your-password"
        self.api_key         = "your-api-key"

        # Services
        self.ecdsa_service   = ECDSAService(self.public_cert_path, self.pkcs12_path, self.pkcs12_password, log)
        self.webhook_service = WebhookService(self.ecdsa_service, log)
        self.api_service     = ApiSubscriptionsService(self.api_username, self.api_password, self.api_key, self.ecdsa_service, log)


    def create_new_subscription(self):
        try:
            # Subscription data
            subscription = {
                ApiSubscriptionsService.WEBHOOK_URL: "https://your-webhook-url",
                ApiSubscriptionsService.ENROLLMENT_ID: str(uuid.uuid1()),
                ApiSubscriptionsService.EVENT_TYPE: "mx.com.circulodecredito.<event-type>"
            }

            webhook_username = "your-secure-username"
            webhook_password = "your-secure-password"

            # Create webhook auth token
            x_webhook_auth = self.webhook_service.generate_auth_token(webhook_username, webhook_password)

            response = self.api_service.createSubscription(x_webhook_auth, subscription)

            log.info(f"API Subscriptions Response Body: {response.text}")

        except Exception as exception:
            log.error(f"Failed to create a new API Subscription. Cause: {exception}")
            traceback.print_exc()

    def find_subscription(self):
        
        subscription_id = "your-subscription-id"

        try:
            response = self.api_service.find_subscription_by_id(subscription_id)

            log.info(f"API Subscriptions Response Body: {response.text}")

        except Exception as exception:
            log.error(f"Failed to find subscription:{subscription_id} in API Subscriptions. Cause: {exception}")
            traceback.print_exc()


api_subscriptions = ApiSubscription()
#api_subscriptions.create_new_subscription()
#api_subscriptions.find_subscription()
