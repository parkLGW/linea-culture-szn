import json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account.account import Account
from loguru import logger


class NFTMint:
    def __init__(self, idx, private_key, rpc, proxies):
        self.idx = idx
        self.address = Account.from_key(private_key).address
        self.private_key = private_key
        self.proxies = proxies
        self.linea_rpc = rpc

    async def mint_on_nfts2me(self, contract_name):
        f = open('abi.json', 'r', encoding='utf-8')
        contract = json.load(f)[contract_name]
        contract_address = Web3.to_checksum_address(contract['address'])
        abi = contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_rpc = w3.eth.contract(address=contract_address, abi=abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract_rpc.functions.mintEfficientN2M_001Z5BWH().estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract_rpc.functions.mintEfficientN2M_001Z5BWH().build_transaction(
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
            f"account {self.idx} mint {contract_name} nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")

    async def mint_on_element(self, contract_name, launchpad_id):
        f = open('abi.json', 'r', encoding='utf-8')
        contract = json.load(f)[contract_name]
        contract_address = Web3.to_checksum_address(contract['address'])
        abi = contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_rpc = w3.eth.contract(address=contract_address, abi=abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract_rpc.functions.launchpadBuy('0x0c21cfbb', launchpad_id, 0, 1, [], b'').estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract_rpc.functions.launchpadBuy('0x0c21cfbb', launchpad_id, 0, 1, [], b'').build_transaction(
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
            f"account {self.idx} mint {contract_name} nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")

    async def mint_yooldo_nft(self):
        f = open('abi.json', 'r', encoding='utf-8')
        yooldo_contract = json.load(f)['yooldo']
        contract_address = Web3.to_checksum_address(yooldo_contract['address'])
        yooldo_abi = yooldo_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=yooldo_abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract.functions.mint().estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract.functions.mint().build_transaction(
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

        logger.info(f"account {self.idx} mint yooldo nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")

    async def mint_acg_nft(self):
        f = open('abi.json', 'r', encoding='utf-8')
        acg_contract = json.load(f)['acg']
        contract_address = Web3.to_checksum_address(acg_contract['address'])
        acg_abi = acg_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=acg_abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract.functions.mint().estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract.functions.mint().build_transaction(
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

        logger.info(f"account {self.idx} mint ACG nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")

    async def mint_sending_me_nft(self):
        f = open('abi.json', 'r', encoding='utf-8')
        sending_me_contract = json.load(f)['sending_me']
        contract_address = Web3.to_checksum_address(sending_me_contract['address'])
        sending_me_abi = sending_me_contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = w3.eth.contract(address=contract_address, abi=sending_me_abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract.functions.mint().estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract.functions.mint().build_transaction(
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
            f"account {self.idx} mint sendingMe nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")

    async def mint_on_mintpad(self, contract_name):
        f = open('abi.json', 'r', encoding='utf-8')
        contract = json.load(f)[contract_name]
        contract_address = Web3.to_checksum_address(contract['address'])
        abi = contract['abi']

        proxies = {"proxies": self.proxies} if self.proxies is not None else None

        w3 = Web3(HTTPProvider(self.linea_rpc, request_kwargs=proxies))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_rpc = w3.eth.contract(address=contract_address, abi=abi)

        nonce = w3.eth.get_transaction_count(account=self.address)

        gas = contract_rpc.functions.mint(self.address, 0, 1, b'').estimate_gas(
            {
                'from': self.address,
                'nonce': nonce,
                'value': 0
            }
        )
        transaction = contract_rpc.functions.mint(self.address, 0, 1, b'').build_transaction(
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
            f"account {self.idx} mint {contract_name} nft success ✅ tx hash: https://lineascan.build/tx/{tx_hash.hex()}")
