from Pyro5.api import expose, serve
import yaml

from receipt_parser import GenAIReceiptParser


def main(args):
    expose(GenAIReceiptParser.parse)
    with open(args.secrets, 'r') as fp:
        key = yaml.safe_load(fp)['llm_api_key']
    genai_parser = GenAIReceiptParser(key, args.model_name)
    serve({genai_parser: 'mysite.receipt_recognizer'})

def parse_args():
    import argparse
    parser = argparse.ArgumentParser('GenAIReceiptOCR')
    parser.add_argument('--secrets', default='./secrets.yaml', help='Key file for gemini model')
    parser.add_argument('--model-name', dest='model_name', default='gemini-1.5-pro-latest', help='Specify Gemini model version with full name')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
