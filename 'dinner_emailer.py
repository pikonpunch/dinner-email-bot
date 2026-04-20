
```python
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import anthropic

# Set up Claude
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

def generate_content():
    prompt = """Generate a daily dinner email for a family with small children. Include:

1. 3 family-friendly dinner ideas (Joanna Gaines/Giada De Laurentiis style - wholesome, approachable, kid-friendly but still good for adults)
2. 1 dad joke

Format as:
🍽️ TONIGHT'S DINNER IDEAS

1. [Dinner idea 1 - include brief description]
2. [Dinner idea 2 - include brief description] 
3. [Dinner idea 3 - include brief description]

😄 Dad Joke of the Day:
[Insert dad joke here]

Keep it warm, friendly, and practical for busy families."""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def send_email(content):
    sender_email = "andrewpetrini@gmail.com"
    sender_password = os.environ['GMAIL_APP_PASSWORD']
    recipient_email = "sckjeldsen@icloud.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Dinner Ideas for {datetime.now().strftime('%B %d, %Y')}"
    
    # Add body to email
    msg.attach(MIMEText(content, 'plain'))
    
    # Gmail SMTP configuration
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()
    
    print(f"Email sent successfully at {datetime.now()}")

if __name__ == "__main__":
    try:
        content = generate_content()
        send_email(content)
    except Exception as e:
        print(f"Error: {e}")
```
