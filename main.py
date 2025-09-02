import hashlib
import json
import time
from flask import Flask, render_template, request #Used for backend in web development
import torch #Used for neural networking
from transformers import T5ForConditionalGeneration, T5Tokenizer #used as an alternate of a proper language model.


'''The below code is for generation of the model which is used as an alternative for a more complex AI model.'''


model_name = 't5-small'
model = T5ForConditionalGeneration.from_pretrained(model_name)# used for generation of text 
tokenizer = T5Tokenizer.from_pretrained(model_name)


'''
The below code basically defines the block and the attributes. 

1)The first fuction is used to define the attributes of the class.
2)The second function is used to generate a hash which is used to identify each block in the blockchain.
3)The third fuction is in the form of JSON so that the attributes of this class can be accessed by the website.


'''
class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'nonce': self.nonce,
            'hash': self.hash
        }

'''
This class defines the blockchain and the functions which are supposed to be performed.

1)The first fuction here is used to define an attribute called 'chain' which is used to create the starting block.
2)The second function is used to create the origin block(This is the function called by the first fuction).
3)The third function is used to create more blocks.
4)The fourth function calls the a fuction from the class Block which is then used to define the attributes of the new block which is
supposed to be added.

Note: There must be an function which validates the data of each Block and makes sure that the data of individual blocks cannot be
changed. This increases the security of the blockchain.
'''

class Blockchain:
    def __init__(self):
        self.chain = [self.create_origin_block()]

    def create_origin_block(self):
        return Block(0, "0", int(time.time()), "Origin Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.index = len(self.chain)
        new_block.previous_hash = self.get_latest_block().hash
        new_block.timestamp = int(time.time())
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def to_dict(self):
        return [block.to_dict() for block in self.chain]
    
'''
This used to generate the nodes of the blockchain. 
Note: Generally this is a alot more complex since multiple different servers are used to host each node
'''

node1 = Blockchain()
node2 = Blockchain()
node3 = Blockchain()
'''The below data is used the generate a generic block.'''

data_to_add = "New data generated"

new_block = Block(0, "0", 0, data_to_add)
node1.add_block(new_block)
node2.add_block(new_block)
node3.add_block(new_block)

print("Block added to all nodes.")

'''
This is the code for the basic AI model which we have used.
It is used the generate a response to the prompt.
'''

def generate_response(prompt, max_length=100):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    with torch.no_grad():
        output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

'''The code for the backend of our website starts from here.'''

app = Flask(__name__)

'''This is the homepage of our website and it shows the blocks present in each node.'''

@app.route('/')
def index():
    return render_template('index.html', node1=node1.chain, node2=node2.chain, node3=node3.chain)

'''This function is used to add a block to each node.'''

@app.route('/add_block', methods=['POST'])
def add_block():
    datax = request.form['data']
    data_to_add = generate_response(datax)
    new_block = Block(0, "0", 0, data_to_add)

    node1.add_block(new_block)
    node2.add_block(new_block)
    node3.add_block(new_block)

    return index()
'''This is used to run the application'''

if __name__ == '__main__':
    app.run(debug=False)
