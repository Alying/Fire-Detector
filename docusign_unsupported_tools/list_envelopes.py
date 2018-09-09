from datetime import datetime
from datetime import timedelta
from docusign_esign import EnvelopesApi

from example_base import ExampleBase


class ListEnvelopes(ExampleBase):

    def list(self):
        self.check_token()

        envelope_api = EnvelopesApi(ListEnvelopes.api_client);
        from_date = (datetime.now() + timedelta(days=-30)).strftime("%Y/%m/%d")
        return envelope_api.list_status_changes(ListEnvelopes.accountID, from_date=from_date)
