import docusign_esign as docusign

from ds_helper import DSHelper
from list_envelopes import ListEnvelopes
from send_envelope import SendEnvelope
from ds_config import DSConfig

def main():
    api_client = docusign.ApiClient()

    CONSENT_REDIRECT_URL = "https://www.docusign.com" # Just used for individual permission request

    try:
        print("\nSending an envelope...")
        result = SendEnvelope(api_client).send_envelope()
        print(f"Envelope status: {result.status}. Envelope ID: {result.envelope_id}")

        print("\nList envelopes in the account...")
        envelopes_list = ListEnvelopes(api_client).list()
        envelopes = envelopes_list.envelopes
        num_envelopes = len(envelopes)
        if num_envelopes > 2:
            print(f"Results for {num_envelopes} envelopes were returned. Showing the first two:\n")
            envelopes_list.envelopes = [envelopes[0], envelopes[1]]
        else:
            print(f"Results for {num_envelopes} envelopes were returned:\n")

        DSHelper.print_pretty_json(envelopes_list)
    except docusign.rest.ApiException as err:
        print ("\n\nDocuSign Exception!")

        # Special handling for consent_required
        body = err.body.decode('utf8')
        if "consent_required" in body:
            consent_scopes = "signature%20impersonation"
            consent_url = f"{DSConfig.auth_server()}/oauth/auth?response_type=code&scope={consent_scopes}&client_id={DSConfig.client_id()}&redirect_uri={CONSENT_REDIRECT_URL}"
            print (f"""
\nC O N S E N T   R E Q U I R E D
Ask the user who will be impersonated to run the following url:
    {consent_url}

It will ask the user to login and to approve access by your application.

Alternatively, an Administrator can use Organization Administration to
pre-approve one or more users.""")
        else:
            print (f"   Reason: {err.reason}")
            print (f"   Error response: {err.body.decode('utf8')}")

    print("\nDone.\n")

if __name__ == "__main__":
    main()
