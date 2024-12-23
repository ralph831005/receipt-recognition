import logging
import json
import os
import yaml

from receipt_parser import GenAIReceiptParser


def main(args):
    with open(args.secrets, 'r') as fp:
        key = yaml.safe_load(fp)['llm_api_key']
    recognizer = GenAIReceiptParser(key, args.model_name)
    result = recognizer.parse(args.image_path)

    # output will be in './output'
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, os.path.basename(args.image_path).split('.', 1)[0] + '_result.json')
    with open(output_path, 'w') as fp:
        fp.write(json.dumps(result))


def parse_args():
    import argparse
    parser = argparse.ArgumentParser('GenAIReceiptOCR')
    parser.add_argument('--secrets', default='./secrets.yaml', help='Key file for gemini model')
    parser.add_argument('--model-name', dest='model_name', default='gemini-1.5-pro-latest', help='Specify Gemini model version with full name')
    parser.add_argument('--image', dest='image_path', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(filename='genai.log', encoding='utf-8', level=logging.DEBUG)
    main(parse_args())
