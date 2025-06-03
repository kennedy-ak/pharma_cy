import requests

def send_sms(phone_number, otp_code):
    """Send an SMS using Mnotify API"""
    message = f"Your pharmacy admin login OTP is: {otp_code}. This code will expire in 10 minutes. Do not share this code with anyone."
    
    # URL-encode the message
    encoded_message = requests.utils.quote(message)

    # Replace with your actual Mnotify API key and registered sender ID
    api_key = ""
    sender_id = "Afimpp-Tvet"
    
    # Construct the URL
    url = f"https://apps.mnotify.net/smsapi?key={api_key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("SMS sent successfully!")
        else:
            print("Failed to send SMS.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


# Example usage
if __name__ == "__main__":
    test_number = "0557782728"      # Replace with the actual phone number
    test_otp = "123456"             # Replace with the actual OTP
    send_sms(test_number, test_otp)
