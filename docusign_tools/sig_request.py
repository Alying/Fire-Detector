from __future__ import absolute_import, print_function
from pprint import pprint
import unittest
import webbrowser

import docusign_esign as docusign
from docusign_esign import AuthenticationApi, TemplatesApi, EnvelopesApi
from docusign_esign.rest import ApiException

user_name = "smit.rao@mail.utoronto.ca"
integrator_key = "0521cc19-0848-42c5-a111-3e5070e7320e"
base_url = "https://demo.docusign.net/restapi"
oauth_base_url = "account-d.docusign.com" # use account.docusign.com for Live/Production
redirect_uri = "https://www.docusign.com/api"
private_key_filename = "keys/docusign_private_key.txt"
user_id = "d744035f-6940-48cf-9e22-b222fc45a86d"
template_id = "717e95da-3de9-4c52-b7d1-38539e132002"

api_client = docusign.ApiClient(base_url)

# IMPORTANT NOTE:
# the first time you ask for a JWT access token, you should grant access by making the following call
# get DocuSign OAuth authorization url:
oauth_login_url = api_client.get_jwt_uri(integrator_key, redirect_uri, oauth_base_url)
# open DocuSign OAuth authorization url in the browser, login and grant access
# webbrowser.open_new_tab(oauth_login_url)
print(oauth_login_url)

# END OF NOTE

# configure the ApiClient to asynchronously get an access token and store it
api_client.configure_jwt_authorization_flow(private_key_filename, oauth_base_url, integrator_key, user_id, 3600)

docusign.configuration.api_client = api_client

template_role_name = 'Owner'

# create an envelope to be signed
envelope_definition = docusign.EnvelopeDefinition()
envelope_definition.email_subject = 'Please Sign my Python SDK Envelope'
envelope_definition.email_blurb = 'Hello, Please sign my Python SDK Envelope.'

# assign template information including ID and role(s)
envelope_definition.template_id = template_id

# create a template role with a valid template_id and role_name and assign signer info
t_role = docusign.TemplateRole()
t_role.role_name = template_role_name
t_role.name ='Smitty Developer'
t_role.email = "rao.smit.2@gmail.com"

sign_here = docusign.SignHere()
sign_here.document_id = '1'
sign_here.page_number = '1'
sign_here.recipient_id = '1'
sign_here.x_position = '100'
sign_here.y_position =  '100'
sign_here.scale_value = '0.5'

text_tab = docusign.Text()
text_tab.tab_label = "Basic"
text_tab.value = "Fire Goodwill Message"

number_tab = docusign.Number()
number_tab.tab_label = "MonitorPay"
number_tab.value = 5.99




tabs = docusign.Tabs()
# tabs.sign_here_tabs = [sign_here]
tabs.text_tabs = [text_tab]
tabs.number_tabs = [number_tab]
t_role.tabs = tabs


# create a list of template roles and add our newly created role
# assign template role(s) to the envelope
envelope_definition.template_roles = [t_role]

# send the envelope by setting |status| to "sent". To save as a draft set to "created"
envelope_definition.status = 'sent'

auth_api = AuthenticationApi()
envelopes_api = EnvelopesApi()

try:
    login_info = auth_api.login(api_password='true', include_account_id_guid='true')
    assert login_info is not None
    assert len(login_info.login_accounts) > 0
    login_accounts = login_info.login_accounts
    assert login_accounts[0].account_id is not None

    base_url, _ = login_accounts[0].base_url.split('/v2')
    api_client.host = base_url
    docusign.configuration.api_client = api_client

    envelope_summary = envelopes_api.create_envelope(login_accounts[0].account_id, envelope_definition=envelope_definition)
    assert envelope_summary is not None
    assert envelope_summary.envelope_id is not None
    assert envelope_summary.status == 'sent'

    print("EnvelopeSummary: ", end="")
    pprint(envelope_summary)

except ApiException as e:
    print("\nException when calling DocuSign API: %s" % e)
    assert e is None # make the test case fail in case of an API exception



