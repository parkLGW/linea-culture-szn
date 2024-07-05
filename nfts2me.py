import json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account.account import Account
from loguru import logger


class NFTs2ME:
    def __init__(self, idx, private_key, rpc, proxies):
        self.idx = idx
        self.address = Account.from_key(private_key).address
        self.private_key = private_key
        self.proxies = proxies
        self.linea_rpc = rpc

    async def mint_wizards_nft(self):
        f = open('abi.json', 'r', encoding='utf-8')
        wizards_contract = json.load(f)['wizards']
        contract_address = Web3.to_checksum_address(wizards_contract['address'])
        wizard_abi = wizards_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=wizard_abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract.functions.mintEfficientN2M_001Z5BWH().estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract.functions.mintEfficientN2M_001Z5BWH().build_transaction(
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

        logger.info(f"account {self.idx} mint wizards nft success ✅ tx hash:{tx_hash.hex()}")

    async def mint_efrogs_nft(self):
        f = open('abi.json', 'r', encoding='utf-8')
        efrogs_contract = json.load(f)['efrogs']
        contract_address = Web3.to_checksum_address(efrogs_contract['address'])
        efrogs_abi = efrogs_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=efrogs_abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract.functions.mintEfficientN2M_001Z5BWH().estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract.functions.mintEfficientN2M_001Z5BWH().build_transaction(
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

        logger.info(f"account {self.idx} mint efrogs nft success ✅ tx hash:{tx_hash.hex()}")
