# demo_oAuthSmtp
A simple script to illustrate how to send outbound emails from an office 365 exchange account in Python via oauth authentication

## Prerequisites 
- Enterprise app created in Entra within the tenant hosting the email account used for sending emails (SENDER)
- Enterprise app granted the admin application access to the SMTP.SendAsApp on the Office 365 Exchange Online API
- Non-expired credential available for the enterprise app (client secret)
- SENDER is allowed to use the [SMTP AUTH](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/authenticated-client-smtp-submission#use-the-microsoft-365-admin-center-to-enable-or-disable-smtp-auth-on-specific-mailboxes)
- Service principal was created on exchange online for the enterprise app, and this service principal was granted full access on the SENDER mailbox

## Config file

A config file needs to be present with the sensitive info you retrieved in the prerequisites. The script expects a `conf.json` file in the working directory, and the the structure should be the following : 
```
{
    "clientId":"<YOUR CLIENT ID>",
    "clientSecret":"<YOUR CLIENT SECRET>",
    "tenantId":"<YOUR TENANT ID>",
    "fromEmail":"<THE SENDER EMAIL>"
}

```
