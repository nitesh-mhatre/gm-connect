from gm_connect.manager import EmailManager

def main():
    manager = EmailManager()

    for i in range(1,10001):
        print(f"Sending test-{i} email...")
        manager.send_email(
            to="mr.psycho.email@gmail.com",  # Replace with a real email
            subject=f"gm-connect Test-{i}",
            body=f"Hello, this is a test email from gm-connect! {str(i)*i}"
        )
        print("Email sent ✅")
    
    manager.close()



if __name__ == "__main__":
    main()
