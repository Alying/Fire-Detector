# Example 1: Python Service Integration

Repository: [eg-01-Python-jwt](https://github.com/docusign/eg-01-Python-jwt)

<!--
## Articles and Screencasts

* Guide: Using OAuth JWT flow with DocuSign.
* Screencast: Using OAuth JWT flow with DocuSign.
* Guide: Sending an envelope with the Node.JS SDK.
* Screencast: Sending an example with Node.JS SDK.
-->

## Introduction

This software is an example of a **System Integration**.
This type of application interacts with DocuSign on its
own. There is no user interface and no user is present
during normal operation.

The application uses the OAuth JWT grant flow to impersonate
a user in the account.

This launcher example includes two examples:
1. Send an html, Word, and PDF file in an envelope to be signed.
1. List the envelopes in the account that are less than 30 days old.

## Installation

This example requires Python v3.6 or later.
The SDK itself works with Python v2.7 or later.

Download or clone this repository. Then:

````
cd eg-01-Python-jwt
pip install docusign_esign

# Create the config file
cp ds_config_EXAMPLE.ini ds_config.ini
````

### Configure the example's settings

You can configure the example either via an .ini file or via
environment variables:

*  **ds_config.ini:** Edit the `ds_config.ini` file in the root
   directory.
   (After creating it from the `ds_config_EXAMPLE.ini` file.)

   **Note:** the private key's second and subsequent
   lines need to have a space added at the beginning due
   to requirements from the Python configuration file
   parser. See the example config file for an example.

   More information for the configuration settings is below.
*  Or via **environment variables:** export the needed
   environment variables. The file `ds_config.py` reads
   the variables.

`ds_config.ini` is in the .gitignore file so your
private information will not be added to your repository.
Do not store your Integration Key, private key, or other
private information in your code repository.

#### Creating the Integration Key
Your DocuSign Integration Key must be configured for a JWT OAuth authentication flow:
* Create a public/private key pair for the key. Store the private key
  in a secure location. You can use a file or a key vault.
* The example requires the private key. Store the private key in the
  `ds_config.ini` file or in the environment variable
  `DS_PRIVATE_KEY`.
* If you will be using individual permission grants, you must create a
  `Redirect URI` for the key. Any URL can be used. By default, this
  example uses `https://www.docusign.com`

#### The impersonated user's guid
The JWT will impersonate a user within your account. The user can be
an individual or a user representing a group such as "HR".

The example needs the guid assigned to the user.
The guid value for each user in your account is available from
the Administration tool in the **Users** section.

To see a user's guid, **Edit** the user's information.
On the **Edit User** screen, the guid for the user is shown as
the `API Username`.

## Run the examples

````
python main.py
````

## Support, Contributions, License

Submit support questions to [StackOverflow](https://stackoverflow.com). Use tag `docusignapi`.

Contributions via Pull Requests are appreciated.
All contributions must use the MIT License.

This repository uses the MIT license, see the
[LICENSE](https://github.com/docusign/eg-01-Python-jwt/blob/master/LICENSE) file.
