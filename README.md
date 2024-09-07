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
4. Go to *Database Access" option on left bar and configure a new user.
5. Now, click on "Database" option on left bar, go to *Browse Collections* and hit on "Create Database". You will be asked for a database name and collection name.
  **E.g.**
  ```python
  Database name: cipherty
  Collection name: enc_data
  ```






6. sdkafkskaksfd



**Author:** @birdm4nw
