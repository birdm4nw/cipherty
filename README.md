<p align="center">
  <img src="captures/cipherty_main2.png" alt="Description of Image" width="500"/>
</p>

# cipherty
**cipherty** is a command line tool written in Python that allows you to safely encrypt and decrypt any type of files by ensuring the complience of CIA triad (confidentiality, integrity and availability) while gives you the option to store encrypted files in a native-cloud Non-Relation Database such as Mongo. 
The encryption system is based in the AES (Advanced Encryption Standard) algorithm, a symmetric block cipher used by the US government to protect classified information.

## Installation
1. Clone the repository

2. Go to the cipherty folder and install requirements by running the following command:
```bash
pip install -r requirements.txt
```

3. Go to the [Mongo Atlas](https://account.mongodb.com/account/login) and create an account in case you hadn't it.

4. Go to **Database Access** option on left bar and configure a new user by assigning a username with a password.

5. Now, click on **Database** option on left bar, go to *Browse Collections* and hit on "Create Database". You will be asked for a database name and collection name.
  **E.g.**
  ```python
  Database name: cipherty
  Collection name: enc_data
  ```

6. Return to **Database** option, click on "Connect" and finally select "Drivers". Copy the URI you see there and paste it on your MONGO_URI variable (located in **.env** file):
  ```python
  MONGO_URI=mongodb+srv://USERNAME:PASSWORD@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
  MONGO_DB=YOUR_DB_NAME
  ```
- Do not forget to replace the username and password with the values configurated in step 4.

7. Finally, go to your **lib/db_operations.py** file within the **cipherty** folder and replace your current "Collection name" in line 24, the one configurated in step 5.

## Usage
```bash
python3 cipherty.py
```

## Samples
<p align="center">
  <img src="captures/encrypted_view.png" alt="Description of Image" width="1000"/>
</p>

## Annexes
<!-- Two images side by side with descriptions underneath -->
<div style="display: flex; justify-content: center;">
  <div style="text-align: center; margin-right: 20px;">
    <img src="captures/cipherty_fstructure.png" alt="Description of Image 1" style="width: 150px;"/>
    <div>Description of Image 1</div>
  </div>
  <div style="text-align: center;">
    <img src="captures/cipherty_fstructure.png" alt="Description of Image 2" style="width: 150px;"/>
    <div>Description of Image 2</div>
  </div>
</div>


**Author:** @birdm4nw
