from gm_connect.manager import EmailManager
from gm_connect.config import Config

def main():
    configuration = Config(env_file="/home/nitesh/repos/gm-connect/gm-connect/.env").load()
    manager = EmailManager(config=configuration)

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
    print(manager.bulk_delete(
        #from_sender='mr.psycho.email@gmail.com',
        days_old=-1,
        folder =  "INBOX"
        ))


    #print(manager.move_email(uid, "[Gmail]/Spam"))
    
    
    manager.close()



if __name__ == "__main__":
    main()
