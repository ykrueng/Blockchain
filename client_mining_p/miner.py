import hashlib
import requests

import sys
import json
from time import time

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    print("Finding proof of work ...")
    start_time = time()
    string_object = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(string_object, proof) is False:
        proof += 1
    end_time = time()
    print(f"Found a proof of work in {end_time-start_time} seconds")
    return proof

def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess_hash)
    return guess_hash[:5] == '00000'


if __name__ == '__main__':
    coins = 0
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        new_proof = proof_of_work(data)
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
        except ValueError:
            print("Error: Non-json response")
            print("Response returned:")
            print(r)
            break

        if data['message'] == 'New Block Forged':
            coins += 1
            print(f'You have mined {coins} coins')
            print(data['transactions'])
        else:
            print(data['message'])