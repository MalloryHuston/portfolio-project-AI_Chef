# AI Chef Search Interface

CS361 Portfolio Project – AI Chef

A food machine that cooks food for you whenever you enter any available recipe you want into the site's search engine. It runs via a command prompt interface and its current microservice is running in the background so that the site users can send customer service emails to the site administrators.

Microservice has been completed by <a href="https://github.com/Jacob-Heinrich/email-microservice">Jacob Heinrich.</a>

<h2>Requirements:</h2>

```
pip install pathlib
pip install pika
pip install email
```
<h2>How to Run Program:</h2>
<h3>Terminal 1</h3>

```
python AI_Chef.py
```
<h3>Terminal 2</h3>

```
cd email-microservice
python emailMicroservice.py
```
<h3>Terminal 3</h3>

```
cd email-microservice
python send.py
```
