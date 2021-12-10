import json
import sys

import requests
from web3 import Web3, HTTPProvider
from web3.logs import IGNORE


class TxSpamer:
    ETHERSCAN_API_KEY = 'NQNBSK7FMWMDN1MZN95HQGQKAVAZ52QH97'
    BROWSER_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Geko/20100101 Firefox/69.0'}

    STAKING_CONTRACT = '0x4cda7DE9dbA2C04178D45054e9bDec8dbc178A27'
    TOKEN_CONTRACT = '0x3e52d7d369ae501891a19ca91b4540bafc750e81'
    LP_TOKEN_CONTRACT = '0x4cda7DE9dbA2C04178D45054e9bDec8dbc178A27'

    GAS_LIMIT = 3000000
    GAS_PRICE = 20

    TOKEN_CONTRACT_ABI = json.loads("""[
    	{
    		"anonymous": false,
    		"inputs": [
    			{
    				"indexed": true,
    				"internalType": "address",
    				"name": "owner",
    				"type": "address"
    			},
    			{
    				"indexed": true,
    				"internalType": "address",
    				"name": "spender",
    				"type": "address"
    			},
    			{
    				"indexed": false,
    				"internalType": "uint256",
    				"name": "value",
    				"type": "uint256"
    			}
    		],
    		"name": "Approval",
    		"type": "event"
    	},
    	{
    		"anonymous": false,
    		"inputs": [
    			{
    				"indexed": true,
    				"internalType": "address",
    				"name": "from",
    				"type": "address"
    			},
    			{
    				"indexed": true,
    				"internalType": "address",
    				"name": "to",
    				"type": "address"
    			},
    			{
    				"indexed": false,
    				"internalType": "uint256",
    				"name": "value",
    				"type": "uint256"
    			}
    		],
    		"name": "Transfer",
    		"type": "event"
    	},
    	{
    		"constant": true,
    		"inputs": [
    			{
    				"internalType": "address",
    				"name": "_owner",
    				"type": "address"
    			},
    			{
    				"internalType": "address",
    				"name": "spender",
    				"type": "address"
    			}
    		],
    		"name": "allowance",
    		"outputs": [
    			{
    				"internalType": "uint256",
    				"name": "",
    				"type": "uint256"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": false,
    		"inputs": [
    			{
    				"internalType": "address",
    				"name": "spender",
    				"type": "address"
    			},
    			{
    				"internalType": "uint256",
    				"name": "amount",
    				"type": "uint256"
    			}
    		],
    		"name": "approve",
    		"outputs": [
    			{
    				"internalType": "bool",
    				"name": "",
    				"type": "bool"
    			}
    		],
    		"payable": false,
    		"stateMutability": "nonpayable",
    		"type": "function"
    	},
    	{
    		"constant": true,
    		"inputs": [
    			{
    				"internalType": "address",
    				"name": "account",
    				"type": "address"
    			}
    		],
    		"name": "balanceOf",
    		"outputs": [
    			{
    				"internalType": "uint256",
    				"name": "",
    				"type": "uint256"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": true,
    		"inputs": [],
    		"name": "decimals",
    		"outputs": [
    			{
    				"internalType": "uint256",
    				"name": "",
    				"type": "uint256"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": true,
    		"inputs": [],
    		"name": "getOwner",
    		"outputs": [
    			{
    				"internalType": "address",
    				"name": "",
    				"type": "address"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": true,
    		"inputs": [],
    		"name": "name",
    		"outputs": [
    			{
    				"internalType": "string",
    				"name": "",
    				"type": "string"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": true,
    		"inputs": [],
    		"name": "symbol",
    		"outputs": [
    			{
    				"internalType": "string",
    				"name": "",
    				"type": "string"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": true,
    		"inputs": [],
    		"name": "totalSupply",
    		"outputs": [
    			{
    				"internalType": "uint256",
    				"name": "",
    				"type": "uint256"
    			}
    		],
    		"payable": false,
    		"stateMutability": "view",
    		"type": "function"
    	},
    	{
    		"constant": false,
    		"inputs": [
    			{
    				"internalType": "address",
    				"name": "recipient",
    				"type": "address"
    			},
    			{
    				"internalType": "uint256",
    				"name": "amount",
    				"type": "uint256"
    			}
    		],
    		"name": "transfer",
    		"outputs": [
    			{
    				"internalType": "bool",
    				"name": "",
    				"type": "bool"
    			}
    		],
    		"payable": false,
    		"stateMutability": "nonpayable",
    		"type": "function"
    	},
    	{
    		"constant": false,
    		"inputs": [
    			{
    				"internalType": "address",
    				"name": "sender",
    				"type": "address"
    			},
    			{
    				"internalType": "address",
    				"name": "recipient",
    				"type": "address"
    			},
    			{
    				"internalType": "uint256",
    				"name": "amount",
    				"type": "uint256"
    			}
    		],
    		"name": "transferFrom",
    		"outputs": [
    			{
    				"internalType": "bool",
    				"name": "",
    				"type": "bool"
    			}
    		],
    		"payable": false,
    		"stateMutability": "nonpayable",
    		"type": "function"
    	}
    ]""")

    URL = 'https://data-seed-prebsc-1-s1.binance.org:8545/'

    POW = 18

    def __init__(self, token_contract=None):
        if token_contract is None:
            token_contract = self.TOKEN_CONTRACT

        self.web3 = Web3(HTTPProvider(self.URL))

        staking_contract_abi = self.__get_contract_abi__()

        self.staking_contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(self.STAKING_CONTRACT),
                                                       abi=staking_contract_abi)
        self.token_contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(token_contract), abi=self.TOKEN_CONTRACT_ABI
        )

    def __generate_tx_fields__(self, user):
        nonce = self.web3.eth.get_transaction_count(user, 'pending')
        chain_id = self.web3.eth.chainId

        return {
            'chainId': chain_id,
            'gas': int(self.GAS_LIMIT),
            'gasPrice': self.web3.toWei(self.GAS_PRICE, 'gwei'),
            'nonce': nonce,
            'from': user,
        }

    def __sign_send_tx__(self, tx_fields, user_priv, contract_tx=None):
        if contract_tx is not None:
            tx = contract_tx.buildTransaction(tx_fields)
            signed = self.web3.eth.account.sign_transaction(tx, user_priv)
        else:
            signed = self.web3.eth.account.sign_transaction(tx_fields, user_priv)

        return self.web3.eth.send_raw_transaction(signed.rawTransaction)

    def __get_contract_abi__(self):
        url = 'https://api-testnet.bscscan.com/api?module=contract&action=getabi&address=' \
              '{contract_address}&apikey={etherscan_api_key}'.format(
            contract_address=self.STAKING_CONTRACT, etherscan_api_key=self.ETHERSCAN_API_KEY)

        res = requests.get(url=url, headers=self.BROWSER_HEADERS)

        return res.json().get('result')

    def __get_user_address__(self, user_priv):
        return self.web3.eth.account.privateKeyToAccount(user_priv.strip()).address

    def __decimals__(self, amount) -> int:
        amount = amount.split('.')

        if len(amount) > 1:
            float_part = amount[1]
            if len(float_part) < self.POW:
                float_part = float_part.ljust(self.POW, '0')

            return int(amount[0] + float_part)

        return int(amount[0]) * 10 ** self.POW

    def staking(self, user_priv, custom_amount):
        # prepare data
        approve_tx_status = 0
        custom_amount = self.__decimals__(custom_amount)

        user = self.__get_user_address__(user_priv)
        tx_fields = self.__generate_tx_fields__(user)

        # check allowance
        approve_tx_status = self.token_contract.functions.allowance(user, self.staking_contract.address).call(tx_fields)

        # if allowance failed
        if not approve_tx_status:
            # approve
            approve = self.token_contract.functions.approve(
                spender=self.staking_contract.address,
                amount=custom_amount)
            tx_hash = self.__sign_send_tx__(tx_fields, user_priv, approve)

            approve_tx = self.web3.eth.wait_for_transaction_receipt(tx_hash.hex())
            approve_tx_status = approve_tx.status

        # call staking
        check_stake = self.staking_contract.functions.enter(custom_amount).call(tx_fields)

        if not isinstance(check_stake, list) or len(check_stake):
            print(user, approve_tx_status)
            raise Exception

        # if staking call was successfull, do staking
        stake = self.staking_contract.functions.enter(custom_amount)
        tx_hash = self.__sign_send_tx__(tx_fields, user_priv, stake)

        # get mintedXRBC
        self.web3.eth.wait_for_transaction_receipt(tx_hash)
        receipt = self.web3.eth.get_transaction_receipt(tx_hash)
        event_filter = self.staking_contract.events.Entered().processReceipt(receipt, errors=IGNORE)
        minted_xrbc = event_filter[-1]['args']['mintedXRBC']

        return user, tx_hash.hex(), approve_tx_status > 0, minted_xrbc

    def can_receive(self, amount):
        return self.staking_contract.functions.canReceive(int(amount)).call()

    def leave(self, user_priv, amount):
        user = self.__get_user_address__(user_priv)
        tx_fields = self.__generate_tx_fields__(user)

        amount = int(amount)

        # call leave
        check_leave = self.staking_contract.functions.leave(amount).call(tx_fields)

        if not isinstance(check_leave, list) or len(check_leave):
            print(user, False)
            raise Exception

        # if leave call was successfull, leave
        leave = self.staking_contract.functions.leave(amount)
        tx_hash = self.__sign_send_tx__(tx_fields, user_priv, leave)

        return tx_hash.hex()

    def transfer(self, user_priv_from, user_priv_to, amount, with_contract=True):
        amount = self.__decimals__(amount)

        user_from = self.__get_user_address__(user_priv_from)
        user_to = self.__get_user_address__(user_priv_to)

        tx_fields = self.__generate_tx_fields__(user_from)

        if with_contract:
            transfer = self.token_contract.functions.transfer(user_to, amount)

            return self.__sign_send_tx__(tx_fields, user_priv_from, transfer).hex()

        tx_fields['to'] = user_to
        tx_fields['value'] = amount

        return self.__sign_send_tx__(tx_fields, user_priv_from).hex()


def split_list(input_list: str) -> list:
    input_data = input_list.split('/')
    input_list = [s.strip().split(',') for s in input_data]
    return input_list


if len(sys.argv) > 1:
    arg1 = sys.argv[1]

    token = None
    if arg1 == 'transfer':
        token = sys.argv[2]

    tx_spamer = TxSpamer(token)

    if arg1 == 'can_receive':
        print(tx_spamer.can_receive(sys.argv[2]))
    elif arg1 == 'leave':
        print(tx_spamer.leave(sys.argv[2], sys.argv[3]))
    elif arg1 == 'leave_all':
        txs_datum = split_list(sys.argv[2])

        for tx_data in txs_datum:
            try:
                print(tx_spamer.leave(tx_data[0], tx_data[1]))
            except Exception as e:
                print(str(e))
                break
    elif arg1 == 'transfer':
        txs_datum = split_list(sys.argv[4])

        for tx_data in txs_datum:
            try:
                print(tx_spamer.transfer(sys.argv[3], tx_data[0], tx_data[1]))
            except Exception as e:
                print(str(e))
                break
    elif arg1 == 'crypto_send':
        txs_datum = split_list(sys.argv[3])

        for tx_data in txs_datum:
            try:
                print(tx_spamer.transfer(sys.argv[2], tx_data[0], tx_data[1], False))
            except Exception as e:
                print(str(e))
                break
    else:
        for_leave = ''
        txs_datum = split_list(sys.argv[1])

        for tx_data in txs_datum:
            try:
                result = tx_spamer.staking(tx_data[0], tx_data[1])
                print(result)
                for_leave += str(result[0]) + ',' + str(result[-1]) + '/'
            # in case of 'nonce too low' repeat transaction while success
            except ValueError as v:
                err_dict = eval(str(v))

                if 'message' in err_dict and err_dict['message'] == 'nonce too low':
                    result = None
                    i = 0
                    while result is None and i < 10:
                        i += 1
                        try:
                            result = tx_spamer.staking(tx_data[0], tx_data[1])
                        except Exception:
                            pass
                    print(result)
                    for_leave += str(result[0]) + ',' + str(result[-1]) + '/'
                else:
                    print(str(v))
                    break
            except Exception as e:
                print(str(e))
                break

        print()
        print(for_leave)
