import requests
import json
import base64
import time
import random

random.seed(time.time())


url = "http://localhost:8383"
rpcuser = "ckrpc"
rpcpassword = "SqqJ1Pu1X3czZSy0zK/tDq8MOvJcxwKfNB0wjqRsbR0="
walletpassword = "asdfasdf"
walletaccount = "mining"
fee = 0
publicKey = "BKlQWrwtPCLrkE99csZ5lPygazvgc8y86cQc5IJtsgu54Pf3ieuGwpkG2qz0jeGsy4PscdAvLO5oyRPyuQS+A04="
miningPubKey = "BBoviCTY1jcAUjJve/rOX75bdIYY615NHTAVf7LUycf+zjaMNyH1HvOwtNKx4gd53jWAbiu+gYuTu7JGpJoolko="
NUM_TX = 10
txperblock = 10

def request(method, params):
	unencoded_str = rpcuser + ":" + rpcpassword
	encoded_str = base64.b64encode(unencoded_str.encode())
	headers = {
		"content-type": "application/json",
		"Authorization": "Basic " + encoded_str.decode('utf-8')
	}
	payload = {
		"method" : method,
		"params": params,
		"jsonrpc": "2.0",
		"id": 0,
	}
	response = requests.post(url, data=json.dumps(payload), headers=headers).json()
	return response


def maketx():

	# retrieve an output to spend
	toSpend = request("listunspentoutputs", {"password": walletpassword, "account": walletaccount})["result"]["outputs"][0]

	# input wrapper spending output
	input = {"outputId": toSpend["id"]}

	# new output for spent funds (minus fee)
	newOutput = {"value": 1000000000 - fee,
        "nonce": random.randint(0, 9999999999999999),
        "data": {"publicKey": publicKey}}

	# the unsigned transaction
	transaction = {
    	"inputs": [input], 
    	"outputs": [newOutput], 
    	"timestamp": int(time.time()),
	}

	# print(json.dumps(transaction, sort_keys=True, indent=4))

	# have ckd sign the unsigned transaction for us
	signed = request("signtransaction", {"transaction": transaction, "password": walletpassword})["result"]
	# print(json.dumps(signed, sort_keys=True, indent=4))

	# broadcast the signed transaction on the network
	success = request("sendrawtransaction", {"transaction": signed})
	print(success)
	return success['result']

	# if(success['result']):
	# 	mined = request("mineblock", {"isBetter": True, "pubKey": miningPubKey})
	# 	# print(mined)

def mine():
	mined = request("mineblock", {"isBetter": True, "pubKey": miningPubKey})
	print(mined)

def main():
	# start_time = time.time()
	# for i in range(NUM_BLOCKS)
	# 	mine(1)
	# end_time = time.time()
	# time_elapsed = end_time - start_time

	# print("time: ", time_elapsed, "\n", 
	# 		"number of blocks: ", NUM_BLOCKS, "\n",
	# 		"number of tx per block: ", 1, "\n"
	# 		"number of tx: ", NUM_TX, "\n",
	# 		"tx / s: ", NUM_TX * 1.0 / (end_time - start_time))

	tot = 0
	for i in range(1):
		var = 10
		start_time = time.time()
		for i in range(var):
			maketx()
			mine()
		end_time = time.time()
		time_elapsed = end_time - start_time
		print(var * 1.0 / time_elapsed)
		tot += var * 1.0 / time_elapsed
	print(tot, tot / 1)

	# mine()

if __name__ == '__main__':
	main()