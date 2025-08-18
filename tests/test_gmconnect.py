from gm_connect.manager import EmailManager

def main():
    manager = EmailManager()

    # ✅ Send test email
    # print("Sending test email...")
    # manager.send_email(
    #     to="n.mhatre90@gmail.com",  # Replace with a real email
    #     subject="gm-connect Test",
    #     body="Hello, this is a test email from gm-connect!"
    # )
    # print("Email sent ✅")

    # ✅ List folders
    print("\nAvailable folders:")
    print(manager.list_folders())

    # ✅ Fetch latest emails
    print("\nFetching latest emails...")
    emails = manager.get_recent_emails(limit=100)
    for e in emails:
        print(f"{e['date']} | {e['from']} | {e['subject']}")
        print("Snippet:", e['snippet'])
        print("-" * 60)

    manager.close()

if __name__ == "__main__":
    main()
