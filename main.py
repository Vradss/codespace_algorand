# import the modules to interactive with the chain
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)
# Create our client
algorand = AlgorandClient.default_local_net()

# dispenser.address = public key | dispenser.signer = private key
dispenser = algorand.account.dispenser()
#print("Dispenser Address:", dispenser.address)

#Create a Wallet & first algorand account
creator = algorand.account.random()
#print("Creator Address:", creator.address)
#print(algorand.account.get_information(creator.address))

#Create first transaction
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

#print(algorand.account.get_information(creator.address))

#Create Token
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="BUILDH3R",
        unit_name="H3R",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
        
    )
)

#Extract asset ID to identify in blockchain
asset_id = sent_txn["confirmation"]["asset-index"]
#print("Asset ID", asset_id)


# Create the receiver
receiver_vrads = algorand.account.random()
#print("Receiver Address:", receiver_vrads.address)

# Transfer the asset from creator to receiver

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_vrads.address,
        amount=10_000_000
    )
)

# The atomic transfer segment : add opt_in
group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_vrads.address,
        asset_id=asset_id
    )
)

group_tx.add_payment(
    PayParams(
        sender=receiver_vrads.address,
        receiver=creator.address,
        amount=1_000_000
    )
)

group_tx.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_vrads.address,
        asset_id=asset_id,
        amount=10
    )
)

group_tx.execute()

#print(algorand.account.get_information(receiver_vrads.address))

print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_vrads.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])

algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=creator.address,
        asset_id=asset_id,
        amount=2,
        clawback_target=receiver_vrads.address
    )
)

print("Post clawback")

print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_vrads.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])