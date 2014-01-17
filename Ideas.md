##Ideas

- Lob email->letter app
 - User registers on our app, store credit card with Stripe, store email in MongoDB
 - When email from known user, parse body as letter with python PDF library, parse subject as address with Google API, paginate, and send as letter through Lob
 - When email from unknown user, prompt for registration
 - Charge stored card when sending letter
- Lob snapchat->postcard
 - Send snapchat to service's username, and have server waiting for incoming messages
 - If snapchat from known user, parse photo as postcard with Python PDF library, and send using Lob as postcard, charging Stripe stored card
 - If unknown user, respond promoting to register
- Email parsing with SendGrid