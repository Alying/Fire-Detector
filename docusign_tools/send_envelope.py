# -*- coding: utf-8 -*-
# coding: utf-8
import base64

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Signer, CarbonCopy, SignHere, Tabs, Recipients, Document

from ds_config import DSConfig
from ds_helper import DSHelper
from example_base import ExampleBase

ENVELOPE_1_DOCUMENT_1 = f"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family:sans-serif;margin-left:2em;">
        <h1 style="font-family: 'Trebuchet MS', Helvetica, sans-serif;
                color: darkblue;margin-bottom: 0;">World Wide Corp</h1>
        <h2 style="font-family: 'Trebuchet MS', Helvetica, sans-serif;
                margin-top: 0px;margin-bottom: 3.5em;font-size: 1em;
                color: darkblue;">Order Processing Division</h2>
        <h4>Ordered by {DSConfig.signer_name()}</h4>
        <p style="margin-top:0em; margin-bottom:0em;">Email:  {DSConfig.signer_email()} </p>
        <p style="margin-top:0em; margin-bottom:0em;">Copy to: {DSConfig.cc_name()}, {DSConfig.cc_email()} </p>
        <p style="margin-top:3em;">
            Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps
            sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon
            drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry.
            Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate
            cake gummies lollipop sugar plum ice cream gummies cheesecake.
        </p>
        <!-- Note the anchor tag for the signature field is in white. -->
        <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
    </body>
</html>
"""

DOC_2_DOCX = "World_Wide_Corp_Battle_Plan_Trafalgar.docx"
DOC_3_PDF = "World_Wide_Corp_lorem.pdf"


def create_document(id, name, file_extension, content):
    """
    create document from HTML content
    :param id:
    :param name:
    :param file_extension:
    :param content:  # either a string or bytes
    :return:
    """

    document = Document()
    if isinstance(content, str):
        content_bytes = content.encode()
    else:
        content_bytes = content

    base64_content = base64.b64encode(content_bytes).decode('ascii')
    document.document_base64 = base64_content
    # can be different from actual file name
    document.name = name
    # Source data format.Signed docs are always pdf.
    document.file_extension = file_extension
    # a label used to reference the doc
    document.document_id = id

    return document


def createSigner():
    signer = Signer()
    signer.email = DSConfig.signer_email()
    signer.name = DSConfig.signer_name()
    signer.recipient_id = "1"
    signer.routing_order = "1"
    return signer


def createCarbonCopy():
    cc = CarbonCopy()
    cc.email = DSConfig.cc_email()
    cc.name = DSConfig.cc_name()
    cc.routing_order = "2"
    cc.recipient_id = "2"
    return cc


def createSignHere(anchor_pattern, anchor_units, anchor_x_offset, anchor_y_offset):
    signHere = SignHere()
    signHere.anchor_string = anchor_pattern
    signHere.anchor_units = anchor_units
    signHere.anchor_x_offset = anchor_x_offset
    signHere.anchor_y_offset = anchor_y_offset
    return signHere


def setSignerTabs(signer1, signers):
    tabs = Tabs()
    tabs.sign_here_tabs = signers
    signer1.tabs = tabs


def createRecipients(signer1, cc1):
    recipients = Recipients()
    recipients.signers = [signer1]
    recipients.carbon_copies = [cc1]
    return recipients


class SendEnvelope(ExampleBase):
    def __init__(self, api_client):
        ExampleBase.__init__(self, api_client)

    def send_envelope(self):
        self.check_token()
        envelope = self.create_envelope()
        envelope_api = EnvelopesApi(SendEnvelope.api_client)
        results = envelope_api.create_envelope(SendEnvelope.accountID, envelope_definition=envelope)
        return results

    def create_envelope(self):
        envelope_definition = EnvelopeDefinition()
        envelope_definition.email_subject = "Please sign this document sent from the Python SDK"

        doc1 = create_document("1", "Order acknowledgement", "html", ENVELOPE_1_DOCUMENT_1)
        doc2 = create_document("2", "Battle Plan", "docx", DSHelper.read_content(DOC_2_DOCX))
        doc3 = create_document("3", "Lorem Ipsum", "pdf", DSHelper.read_content(DOC_3_PDF))

        # The order in the docs array determines the order in the envelope
        envelope_definition.documents = [doc1, doc2, doc3]
        # create a signer recipient to sign the document, identified by name and email
        # We're setting the parameters via the object creation
        signer1 = createSigner()
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

        # create a cc recipient to receive a copy of the documents, identified by name and email
        # We're setting the parameters via setters
        cc1 = createCarbonCopy()
        # Create signHere fields (also known as tabs) on the documents,
        # We're using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope's
        # documents for matching anchor strings. So the
        # sign_here_2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs.
        sign_here1 = createSignHere("**signature_1**", "pixels", "20", "10")
        sign_here2 = createSignHere("/sn1/", "pixels", "20", "10")
        # Tabs are set per recipient / signer
        setSignerTabs(signer1, [sign_here1, sign_here2])
        # Add the recipients to the envelope object
        recipients = createRecipients(signer1, cc1)
        envelope_definition.recipients = recipients
        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        envelope_definition.status = "sent"

        return envelope_definition

