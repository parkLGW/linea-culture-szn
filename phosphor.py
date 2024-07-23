import json
from web3 import Web3, HTTPProvider
from loguru import logger
from web3.middleware import geth_poa_middleware
from eth_account.account import Account
from curl_cffi.requests import AsyncSession, BrowserType


class Phosphor:
    def __init__(self, idx, private_key, user_agent, rpc, proxies):
        self.idx = idx
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://app.phosphor.xyz',
            'priority': 'u=1, i',
            'referer': 'https://app.phosphor.xyz/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
        }
        self.private_key = private_key
        self.address = Account.from_key(private_key).address
        self.proxies = proxies
        self.sess = AsyncSession(
            proxies=self.proxies,
            impersonate=BrowserType.chrome120
        )
        self.linea_rpc = rpc

    async def purchase_intents(self):
        headers = self.headers
        json_data = {
            'buyer': {
                'eth_address': self.address,
            },
            'listing_id': 'fceb2be9-f9fd-458a-8952-9a0a6f873aff',
            'provider': 'MINT_VOUCHER',
            'quantity': 1,
        }

        response = await self.sess.post('https://public-api.phosphor.xyz/v1/purchase-intents', headers=headers,
                                        json=json_data)

        if response.status_code != 201:
            raise Exception(f'account {self.idx} Failed to get purchase_intents data❌')

        res = json.loads(response.text)
        await self._mint_onchain(res['data'])

    async def _mint_onchain(self, purchase_data):
        f = open('abi.json', 'r', encoding='utf-8')
        coop_records_contract = json.load(f)['coop_records']
        contract_address = Web3.to_checksum_address(coop_records_contract['address'])
        coop_records_abi = coop_records_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=coop_records_abi)

        voucher = (
            purchase_data['voucher']['net_recipient'],
            purchase_data['voucher']['initial_recipient'],
            int(purchase_data['voucher']['initial_recipient_amount']),
            int(purchase_data['voucher']['quantity']),
            int(purchase_data['voucher']['nonce']),
            int(purchase_data['voucher']['expiry']),
            int(purchase_data['voucher']['price']),
            int(purchase_data['voucher']['token_id']),
            purchase_data['voucher']['currency'],
        )

        nonce = w3.eth.get_transaction_count(account=self.address)
        gas = contract.functions.mintWithVoucher(voucher, w3.to_bytes(hexstr=purchase_data['signature'])).estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract.functions.mintWithVoucher(voucher,
                                                         w3.to_bytes(
                                                             hexstr=purchase_data['signature'])).build_transaction(
            {
                'from': self.address,
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
                'gas': gas,
                'value': 0
            }
        )
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

        logger.info(
            f"account {self.idx} mint coop records nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")
