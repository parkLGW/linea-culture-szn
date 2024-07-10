import re
import json
from loguru import logger
from faker import Faker
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account.account import Account
from curl_cffi.requests import AsyncSession, BrowserType


class ClutchPlay:
    def __init__(self, idx, private_key, user_agent, rpc, proxies):
        self.idx = idx
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-HK,zh-TW;q=0.9,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://beta.clutchplay.ai',
            'Referer': 'https://beta.clutchplay.ai/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': user_agent,
            'network-id': '59144',
            'network-name': 'Linea Mainnet',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.private_key = private_key
        self.address = Account.from_key(private_key).address
        self.proxies = proxies
        self.sess = AsyncSession(
            proxies=self.proxies,
            impersonate=BrowserType.chrome120
        )
        self.linea_rpc = rpc

    async def _get_signature(self, refer_url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-HK,zh-TW;q=0.9,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.headers['User-Agent'],
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        # response = await self.sess.get('https://beta.clutchplay.ai/profile', headers=headers)
        response = await self.sess.get(refer_url, headers=headers)
        text = response.text.replace(r'\"', '"')
        pattern = r'"signature":"(.*?)"'

        matches = re.findall(pattern, text)
        if not matches:
            raise Exception('No signature found')

        return matches[0]

    async def login(self):
        signature = await self._get_signature('https://beta.clutchplay.ai')
        self.headers.update({
            'signature': signature
        })
        headers = self.headers.copy()
        headers.update({
            'x-initiator': 'web',
        })

        json_data = {
            'wallet_address': self.address,
        }

        response = await self.sess.post('https://v1.api.clutchplay.ai/user/wallet', headers=headers, json=json_data)

        if response.status_code != 200:
            raise Exception(f'account {self.idx} Failed to login❌')

        res = response.json()
        self.headers['Authorization'] = f'Bearer {res["result"]["access_token"]}'
        logger.info(f'account {self.idx} ClutchPlay login success✅')

    async def generate(self, model_id, campaign_id):
        headers = self.headers.copy()

        random_str = Faker().user_name()
        json_data = {
            'model_id': model_id,
            'prompt': f'a photo of ohwx crazy  {random_str}',
            'variations': 1,
            'campaign_id': campaign_id,
        }

        response = await self.sess.post('https://v1.api.clutchplay.ai/generate', headers=headers, json=json_data)

        if response.status_code != 200:
            raise Exception(f'account {self.idx} Failed to generate❌')

        logger.info(f'account {self.idx} ClutchPlay generate success✅: {response.json()["result"]}')

    async def get_campaigns_data(self):
        headers = self.headers.copy()
        headers.update({
            'x-initiator': 'web',
        })

        params = {
            'live': 'true',
        }

        response = await self.sess.get('https://v1.api.clutchplay.ai/campaigns', params=params, headers=headers)

        if response.status_code != 200:
            raise Exception(f'account {self.idx} Failed to get campaign data❌')

        return response.json()['result'][0]

    async def get_collections(self):
        signature = await self._get_signature('https://beta.clutchplay.ai/profile')
        self.headers.update({
            'signature': signature
        })
        headers = self.headers.copy()

        params = {
            'limit': '8',
            'page': '1',
            'tag': 'date',
        }

        response = await self.sess.get('https://v1.api.clutchplay.ai/collections', params=params, headers=headers)

        if response.status_code != 200:
            raise Exception(f'account {self.idx} Failed to get collections❌')

        return response.json()['result']['collection']

    async def upload_img(self, img_url, collection_id):
        headers = self.headers.copy()

        json_data = {
            'image_url': img_url,
            'name': Faker().user_name(),
            'description': Faker().user_name(),
            'collection_id': collection_id,
        }

        response = await self.sess.post('https://v1.api.clutchplay.ai/ipfs', headers=headers, json=json_data)

        if response.status_code != 200:
            Exception(f'account {self.idx} Failed to upload image❌')

        return response.json()['file_url']

    async def mint_clutch_ai_nft(self, img_uri, collection_id):
        headers = self.headers.copy()

        tx_hash = self._mint_onchain(img_uri)

        json_data = {
            'tx_hash': tx_hash,
            'collection_id': collection_id,
        }

        response = await self.sess.post('https://v1.api.clutchplay.ai/nft', headers=headers, json=json_data)

        if response.status_code != 200:
            Exception(f'account {self.idx} Failed to get collections❌')

        logger.info(f'account {self.idx} minted NFT success✅: {response.json()["result"]}')

    def _mint_onchain(self, uri):
        f = open('abi.json', 'r', encoding='utf-8')
        clutch_ai_contract = json.load(f)['clutch_ai']
        contract_address = Web3.to_checksum_address(clutch_ai_contract['address'])
        clutch_ai_abi = clutch_ai_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=clutch_ai_abi)

        nonce = w3.eth.get_transaction_count(account=self.address)
        value = w3.to_wei(0.00012, 'ether')
        gas = contract.functions.safeMint(self.address, uri).estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': value
            }
        )
        transaction = contract.functions.safeMint(self.address, uri).build_transaction(
            {
                'from': self.address,
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
                'gas': gas,
                'value': value
            }
        )
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_hash.hex()
