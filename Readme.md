## Setting up the environment
1. **Clone repository and installing virtual environment:** 
- Open terminal and run the following code one by one :
```
git clone https://github.com/Tushar-04/AmazonScraping.git
```

- If virtualenv not installed in your system :

```
pip install virtualenv
```
2. **Running virtual environment:**

```
cd .\AmazonScraping\
```

```
virtualenv venv
```
- Following code will enable virtual environment
```
.\venv\Scripts\activate
```
- Note: If you get any errors in the above command, run the following command in powershell as admin, else move to the next step.
```
Set-ExecutionPolicy RemoteSigned
```

3. **Instaling dependencies:**

```
pip install -r requirements.txt
```
4. **Running the code**
- Now run the following command in terminal where your virtual environment is running
```
py .\main.py
```
