# 📌 Email Management Module - TODO

## ✅ Phase 1: Core Features (MVP)
- [ x ] 🟢 **Read Emails**
  - Connect via IMAP/POP3
  - Fetch unread/all emails
  - Parse subject, sender, receiver, body, attachments
- [ x ] 🟢 **Send Emails**
  - Send plain text emails
  - Send emails with attachments
- [ x ] 🟢 **Delete Emails**
  - Delete single email by ID
  - Bulk delete (older than X days, from specific sender)
- [ ] 🟢 **Organize / Tag Emails**
  - Move to folders (Inbox, Spam, Custom)
  - Manual tagging (Work, Personal, Finance)
- [ ] 🟡 **Search & Filter**
  - Search by subject, sender, date range
  - Filter unread/read emails

---

## 🚀 Phase 2: Enhanced Features
- [ ] 🟡 **Smart Tagging**
- [ ] 🟡 **Email Prioritization**
- [ ] 🟡 **Scheduling & Automation**
- [ ] 🟡 **Attachment Management**

---

## 🤖 Phase 3: Advanced Features
- [ ] 🟡 **Analytics & Insights**
- [ ] 🟡 **Integrations**
- [ ] 🔴 **Advanced Search**
- [ ] 🔴 **Security**

---

## 🌍 Phase 4: User Experience
- [ ] 🟡 **Multi-Account Support**
- [ ] 🔴 **Offline Mode**
- [ ] 🟡 **CLI Interface**
  - `emailmgr read` → fetch emails  
  - `emailmgr send --to x@y.com --subject "Hi"`  
  - `emailmgr delete --id 123`  
  - `emailmgr tag --id 123 --tag Work`  
- [ ] 🔴 **Web Dashboard**

---

## 🔧 Non-Functional Requirements
- [ x ] 🟢 Secure credential storage (`keyring`, `.env`)
- [ x ] 🟢 Config-driven (JSON/YAML for IMAP/SMTP settings)
- [ ] 🟡 Logging & error handling
- [ ] 🟡 Scalable (handle large inboxes with pagination)

---

## 📦 Packaging & Distribution
- [ x ] 🟢 Create `pyproject.toml` with **Poetry / Hatch / setuptools**
- [ ] 🟢 Package should be **installable from pip**
- [ ] 🟢 Provide importable module:

  ```python
  from gm_connect import EmailClient

  client = EmailClient()
  client.read_emails()


## 📂 Proposed Folder Structure

```bash
project-root/
├── pyproject.toml   # Build + dependencies (standard)
├── README.md        # Docs
├── LICENSE
├── TODO.md
├── .env.example
│
├── src/             # Actual package code
│   └── emailmgr/
│       ├── __init__.py
│       ├── client.py
│       ├── reader.py
│       ├── sender.py
│       ├── manager.py
│       ├── config.py
│       ├── utils.py
│       └── cli.py
│
├── tests/           # Unit tests
└── examples/        # Example usage

