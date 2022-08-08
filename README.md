# AI Chef User Interface

CS361 Portfolio Project – AI Chef

A web service that cooks food for you whenever you enter any available recipe you want into the site's database directory. It runs via a command prompt interface and its current microservice is running in the background so that the site users can send customer service emails to the site administrators.

Microservice has been completed by <a href="https://github.com/Jacob-Heinrich/email-microservice">Jacob Heinrich.</a>

<h3>Requirements:</h3>

```
pip install pathlib
pip install pika
pip install email
```
<h3>How to Run Program:</h3>
<h4>Terminal #1</h4>

```
python AI_Chef.py
```
<h4>Terminal #2</h4>

```
cd email-microservice
python emailMicroservice.py
```
<h4>Terminal #3</h4>

```
cd email-microservice
python send.py
```
