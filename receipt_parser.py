import abc
import json
import logging
import os

import google.generativeai as genai


class ReceiptParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, image_path):
        raise NotImplementedError


class GenAIReceiptParser(ReceiptParser):
    '''
    An gemini based solution for receipt photo processing.
    This needs a gemini api key for querying the llm model.
    '''
    TASK = '''List all the items and prices in the receipt. List the store name, total price, tax, tax rate, and purchase date.'''
    SCHEMA = [
        "Item = {'item': str, 'price': float}",
        "Receipt = {'store': str, 'total_price': float, 'tax': float, 'tax_rate': float, 'purchase_date': str, 'items': list[Item]}",
        "Return: Receipt"
    ]
    VALID_MODELNAME = set(['gemini-1.5-pro-latest', 'gemini-2.0-flash-exp'])

    def __init__(self, key, model_name, check_integration=False):
        assert model_name in self.VALID_MODELNAME
        genai.configure(api_key=key)
        self.prompt = '\n'.join((
            self.TASK, 'Use this JSON schema:',
            *self.SCHEMA
        ))
        self.model = genai.GenerativeModel(model_name=model_name)
        self.logger = logging.getLogger('GenAIReciptOCR')
        self.check_integration = check_integration

    def parse(self, image_path):
        '''
        Upload image and query for item and price.
        '''
        uploaded_file = genai.upload_file(path=image_path, display_name=os.path.basename(image_path))

        self.logger.info(f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}")

        self.logger.info(f"Start query Gemini for receipt recognition")
        response = self.model.generate_content([uploaded_file, self.prompt])
        self.logger.info(f"Query done")

        receipt = json.loads(response.text.strip('`').split('\n', 1)[1])
        if self.check_integration:
            # verbose only
            try:
                self.check(receipt)
            except ValueError as value_err:
                print(value_err)
        return receipt

    def check(self, receipt):
        sum_prices = sum(item['price'] for item in receipt['items'])
        sum_prices_after_tax = sum_prices + receipt['tax']
        if sum_prices_after_tax != receipt['total_price']:
            raise ValueError(f"Total price doesn't match!! Total price is: {receipt['total_price']}, "
                              "tax is {receipt['tax']}, and the sum of items is {sum_prices}")
