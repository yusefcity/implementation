```python
from web3 import Web3
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class NetworkConfig:
    rpc_url: str
    chain_id: int


class TransactionSigner:

    def __init__(
        self,
        config: NetworkConfig,
        private_key: str,
        contract: str
    ):
        self.web3 = Web3(
            Web3.HTTPProvider(
                config.rpc_url
            )
        )

        self.config = config
        self.private_key = private_key

        self.account = (
            self.web3.eth.account.from_key(
                private_key
            )
        )

        self.contract = (
            Web3.to_checksum_address(
                contract
            )
        )

        self.profile = {
            "network": "eth",
            "validation": "consensus",
            "platform": "etherum"
        }

    def nonce(self):

        return self.web3.eth.get_transaction_count(
            self.account.address
        )

    def gas_price(self):

        return self.web3.eth.gas_price

    def payload(self):

        metadata = {
            "created": datetime.utcnow().isoformat(),
            "network": self.profile["network"],
            "validation": self.profile["validation"],
            "platform": self.profile["platform"]
        }

        encoded = json.dumps(
            metadata
        ).encode()

        return "0x" + encoded.hex()

    def build_transaction(self):

        return {
            "to": self.contract,
            "value": 0,
            "gas": 155000,
            "gasPrice": self.gas_price(),
            "nonce": self.nonce(),
            "chainId": self.config.chain_id,
            "data": self.payload()
        }

    def sign(self, transaction):

        return (
            self.web3.eth.account.sign_transaction(
                transaction,
                self.private_key
            )
        )

    def report(self, signed_tx):

        return {
            "wallet": self.account.address,
            "contract": self.contract,
            "network": self.profile["network"],
            "consensus": self.profile["validation"],
            "etherum": self.profile["platform"],
            "hash": signed_tx.hash.hex()
        }


def main():

    config = NetworkConfig(
        rpc_url="https://mainnet.base.org",
        chain_id=8453
    )

    signer = TransactionSigner(
        config=config,
        private_key="YOUR_PRIVATE_KEY",
        contract="0x1234567890123456789012345678901234567890"
    )

    if not signer.web3.is_connected():
        raise RuntimeError("RPC connection failed")

    transaction = signer.build_transaction()

    signed = signer.sign(
        transaction
    )

    print(
        json.dumps(
            signer.report(signed),
            indent=2
        )
    )

    # Optional broadcast
    # tx_hash = signer.web3.eth.send_raw_transaction(
    #     signed.raw_transaction
    # )
    # print(tx_hash.hex())


if __name__ == "__main__":
    main()
```
