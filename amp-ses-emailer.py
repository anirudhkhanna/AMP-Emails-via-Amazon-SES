#!/usr/bin/env python

# Using `x-amp-html` MIME Type to send dynamic AMP emails using Amazon SES.
# Refer: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Replace sender@yourdomain.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Sender Name <sender@yourdomain.com>"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT = "recipient@example.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# `ConfigurationSetName=CONFIGURATION_SET` argument below.
# CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"

# The subject line for the email.
SUBJECT = "Hey, Wizard! Check out this dynamic email."

# The plaintext email body for recipients with non-HTML email clients.
BODY_TEXT = "Lumos! In plain text."

# The HTML email body for recipients with non-AMP email clients.
BODY_HTML = """\
<html>
<body>
  <p>Expelliarmus! In HTML.</p>
</body>
</html>
"""

# The AMPHTML email body for recipients with AMP-supporting email clients.
BODY_AMPHTML = """\
<!doctype html>
<html amp4email>
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
</head>
<body>
  <p>Alohomora! In AMP. :)</p>
</body>
</html>
"""

# The character encoding for the email.
# CHARSET = "utf-8"
CHARSET = "us-ascii"

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)

# Create a multipart/mixed parent container.
msg = MIMEMultipart('mixed')

# Add the Subject, From and To lines.
msg['Subject'] = SUBJECT 
msg['From'] = SENDER 
msg['To'] = RECIPIENT

# Create a multipart/alternative child container.
msg_body = MIMEMultipart('alternative')

# Encode the text and HTML content and set the character encoding. This step is
# necessary if you're sending a message with characters outside the ASCII range.
textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
amphtmlpart = MIMEText(BODY_AMPHTML.encode(CHARSET), 'x-amp-html', CHARSET)

# Add the text and HTML parts to the child container.
msg_body.attach(textpart)
msg_body.attach(htmlpart)
msg_body.attach(amphtmlpart)

# Attach the multipart/alternative child container to the multipart/mixed
# parent container.
msg.attach(msg_body)
# print(msg);

try:
    #Provide the contents of the email.
    response = client.send_raw_email(
        Source=SENDER,
        Destinations=[
            RECIPIENT
        ],
        RawMessage={
            'Data':msg.as_string(),
        },
        # ConfigurationSetName=CONFIGURATION_SET
    )
# Display an error if something goes wrong.	
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])
