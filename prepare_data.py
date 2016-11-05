import mailbox
import os
import json
import re

toplevel_dir = os.path.dirname(os.path.realpath(__file__))
rawdata_dir = os.path.join(toplevel_dir, "Takeout", "Mail")
cleaned_dir = os.path.join(toplevel_dir, "CleanedData")

unicode_and_newlines = re.compile(r"(?:=(?:[(?:A-F|0-9)]{2})?)|\n|\r")

def read_messages(mbox_path):
    def get_text(email):
        payload = email.get_payload()
        while type(payload) is not str:
            payload = payload[0].get_payload()
        return unicode_and_newlines.sub("", payload)

    emails = mailbox.mbox(mbox_path)
    return [{"date": email["Date"], "subject": email["Subject"], "body": get_text(email)} for email in emails]


def retrieve_data():
    data = {}
    for mbox_filename in os.listdir(rawdata_dir):
        party, candidate = mbox_filename.replace(".mbox", "").split("-")
        messages = read_messages(os.path.join(rawdata_dir, mbox_filename))
        data[candidate] = {"candidate": candidate, "party": party, "messages": messages}
    return data


def write_data():
    data = retrieve_data()
    for entry in data.values():
        with open(os.path.join(cleaned_dir, entry['candidate']), 'w') as ofile:
            ofile.write(json.dumps(entry))

if __name__ == "__main__":
    write_data()