import re

with open ("harrypotter01.txt","r" ,encoding= "utf-8") as f:
    raw_text = f.read()

my_symbols = r"([!@#$%^&*()_+{}\[\]\\\":;,.<>/?\s]+)"
token_text = re.split(my_symbols,raw_text)
token_text = [text.strip() for text in token_text if text.strip()]
token_text = sorted(set(token_text))
token_text.extend(["<|endoftext|>","<|unk|>"])

vocabulary = {token:i for i,token in enumerate(token_text)}

class Tokenizer1:
    def __init__(self,sentense):
        self.sentense = sentense
        self.id = {i:s for s,i in sentense.items()}
        self.my_symbols = r"([!@#$%^&*()_+{}\[\]\\\":;,.<>/?\s]+)"

    def encoder(self,text):
        token_id = re.split(self.my_symbols,text)
        token_id = [word.strip() for word in token_id if word.strip()]
        token_id = [word if word in self.sentense else "<|unk|>" for word in token_id]
        token_id = [self.sentense.get(s,self.sentense["<|unk|>"]) for s in token_id]
        return token_id
    
    def decoder(self,id):
        token_text = [self.id.get(i,"<|unk|>") for i in id]
        token_text = " ".join(token_text)
        complete_text = re.sub(r"\s+([!@#$%^&*()_+|~`=\\\[\]{};:'\",.<>/?])",r"\1",token_text)
        return complete_text

tokenizer = Tokenizer1(vocabulary)

sentense ="their greatest fear was puru"
token_id = tokenizer.encoder(sentense)
print(token_id)

token_text = tokenizer.decoder([6418, 3696, 3262, 6859, 7147])
print (token_text)