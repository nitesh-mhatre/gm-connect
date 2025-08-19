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
    emails = manager.get_recent_emails(limit=1)
    for e in emails:
        print(f"{e}")
        print("-" * 60)
        uid = e['uid']

    print('deleting mails................')
    print(manager.bulk_delete(days_old=1))


    #print(manager.move_email(uid, "[Gmail]/Spam"))
    
    
    manager.close()



if __name__ == "__main__":
    main()
